import puppeteer from 'puppeteer';
const b = await puppeteer.launch({headless:true,args:['--no-sandbox']});
const p = await b.newPage();
for (const w of [390,600,900,1024,1280,1440,1711,1920]) {
  await p.setViewport({width:w,height:900,deviceScaleFactor:1});
  await p.goto('http://localhost:3400',{waitUntil:'domcontentloaded'});
  await new Promise(r=>setTimeout(r,400));
  const rows = await p.evaluate(()=>[...document.querySelectorAll('.two-tone')].map(h=>{
    const cs=getComputedStyle(h);
    const lh=parseFloat(cs.lineHeight)||parseFloat(cs.fontSize)*1.02;
    const want=h.querySelectorAll('br').length+1;
    const got=Math.round(h.getBoundingClientRect().height/lh);
    return {sec:h.closest('section')?.id||'?', want, got,
            col:Math.round(h.parentElement.getBoundingClientRect().width),
            fs:Math.round(parseFloat(cs.fontSize))};
  }));
  console.log(`\n--- ${w}px ---`);
  for (const r of rows)
    console.log(`  ${(r.sec+'            ').slice(0,12)} want ${r.want}  got ${r.got}  ${r.got>r.want?'<-- OVERFLOWS':''}  (col ${r.col}px, font ${r.fs}px)`);
}
await b.close();
