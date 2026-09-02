import puppeteer from 'puppeteer';
const b=await puppeteer.launch({headless:true,args:['--no-sandbox']});
const p=await b.newPage();
for (const f of ['','21700.html','high-density.html','ev-packs.html']) {
  const errs=[]; p.removeAllListeners('pageerror'); p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://localhost:3400/'+f,{waitUntil:'networkidle2'});
  await new Promise(r=>setTimeout(r,500));
  const r=await p.evaluate(()=>{
    const hs=[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>+h.tagName[1]);
    let skips=0; for(let i=1;i<hs.length;i++) if(hs[i]-hs[i-1]>1) skips++;
    return {h1:document.querySelectorAll('h1').length, headings:hs.length, skips,
            title:document.title.length, desc:(document.querySelector('meta[name=description]')||{}).content?.length||0,
            canonical:!!document.querySelector('link[rel=canonical]'),
            lang:document.documentElement.lang,
            imgsNoAlt:[...document.images].filter(i=>!i.hasAttribute('alt')).length};});
  console.log(`${(f||'index.html').padEnd(20)} h1=${r.h1} headings=${r.headings} skips=${r.skips} `+
              `title=${r.title}ch desc=${r.desc}ch canonical=${r.canonical} lang=${r.lang} imgs-no-alt=${r.imgsNoAlt} js-errors=${errs.length}`);
}
// robots + sitemap reachable
for (const u of ['robots.txt','sitemap.xml','llms.txt']) {
  const res=await p.goto('http://localhost:3400/'+u);
  console.log(`${u.padEnd(20)} HTTP ${res.status()}`);
}
await b.close();
