import puppeteer from 'puppeteer';
const b=await puppeteer.launch({headless:true,args:['--no-sandbox']});
const p=await b.newPage();
const bad=[]; const seen=new Set();
for (const page of ['index.html','21700.html','high-density.html','ev-packs.html']) {
  await p.goto('http://localhost:3400/'+page,{waitUntil:'networkidle2'});
  await new Promise(r=>setTimeout(r,700));
  const errs=[];
  p.removeAllListeners('pageerror'); p.on('pageerror',e=>errs.push(e.message));
  const links=await p.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')));
  // lazy images below the fold have naturalWidth 0 until scrolled — fetch them instead
  const imgs=await p.evaluate(()=>[...new Set([...document.querySelectorAll('img')].map(i=>i.getAttribute('src')))]);
  for (const src of imgs) {
    const st=await p.evaluate(async u=>{try{const x=await fetch(u,{method:'HEAD'});return x.status;}catch(e){return 0;}}, src);
    if(st!==200) bad.push(`${page}: BROKEN IMG ${src} -> HTTP ${st}`);
  }
  for (const h of links) {
    if (h.startsWith('#') ) {
      const ok=await p.evaluate(id=>!!document.querySelector(id), h==='#top'?'#top':h);
      if(!ok) bad.push(`${page}: dead anchor ${h}`);
      continue;
    }
    if (h.startsWith('tel:')||h.startsWith('mailto:')||h.startsWith('data:')) continue;
    const url='http://localhost:3400/'+h.split('#')[0];
    if(seen.has(url)) continue; seen.add(url);
    const r=await p.evaluate(async u=>{try{const x=await fetch(u,{method:'HEAD'});return x.status;}catch(e){return 0;}},url);
    if(r!==200) bad.push(`${page}: ${h} -> HTTP ${r}`);
  }
  console.log(`${page}: ${links.length} links, ${imgs.length} images, ${errs.length} js errors`);
  errs.forEach(e=>bad.push(`${page}: JS ${e}`));
}
console.log(bad.length? '\nPROBLEMS:\n'+bad.join('\n') : '\nAll links, anchors and images OK');
await b.close();
