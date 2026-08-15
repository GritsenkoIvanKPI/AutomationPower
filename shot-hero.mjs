import puppeteer from 'puppeteer';
const b = await puppeteer.launch({headless:true,args:['--no-sandbox']});
const p = await b.newPage();
await p.setViewport({width:1711,height:980,deviceScaleFactor:1});
await p.goto('http://localhost:3400',{waitUntil:'networkidle2'});
await new Promise(r=>setTimeout(r,1500));
await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible')));
await new Promise(r=>setTimeout(r,700));
for (const i of [0,1,2]) {
  await p.evaluate(n=>document.querySelectorAll('.hero-tab')[n].click(), i);
  await new Promise(r=>setTimeout(r,1400));
  await p.screenshot({path:`temporary screenshots/slide-${i}.png`, clip:{x:0,y:0,width:1711,height:1000}});
  const st = await p.evaluate(()=>({
    word: [...document.querySelectorAll('.hero-swap-item')].findIndex(e=>e.classList.contains('is-active')),
    shot: [...document.querySelectorAll('.hero-shot')].findIndex(e=>e.classList.contains('is-active')),
    tab:  [...document.querySelectorAll('.hero-tab')].findIndex(e=>e.getAttribute('aria-selected')==='true'),
    link: document.getElementById('heroLink').getAttribute('href'),
    chip: document.getElementById('heroChip').textContent.trim(),
  }));
  console.log(i, JSON.stringify(st));
}
const ov = await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
console.log('overflowX', ov);
await b.close();
