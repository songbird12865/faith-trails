(() => {
  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  let active=gameplay, muted=localStorage.getItem('ft-muted')==='1';
  const fade=(el,to,ms=500)=>{const from=el.volume,at=performance.now();const tick=n=>{const p=Math.min(1,(n-at)/ms);el.volume=from+(to-from)*p;if(p<1)requestAnimationFrame(tick)};requestAnimationFrame(tick)};
  function syncToggle(){if(toggle){toggle.textContent=muted?'♪':'♫';toggle.setAttribute('aria-label',muted?'Turn music on':'Turn music off')}}
  async function unlock(){gate?.classList.add('is-hidden');sessionStorage.setItem('ft-audio-unlocked','1');gameplay.volume=0;gameplay.muted=muted;try{await gameplay.play();fade(gameplay,.32,700)}catch(e){} }
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio={
    duck(){fade(active,.06,250)},unduck(){fade(active,active===celebration?.40:.32,350)},
    celebrate(){if(!celebration)return;fade(gameplay,0,400);setTimeout(()=>{gameplay.pause();celebration.currentTime=0;celebration.volume=0;celebration.muted=muted;celebration.play().catch(()=>{});fade(celebration,.4,650);active=celebration},380)},
    gameplay(){if(!gameplay)return;fade(celebration,0,350);setTimeout(()=>{celebration.pause();gameplay.volume=0;gameplay.muted=muted;gameplay.play().catch(()=>{});fade(gameplay,.32,650);active=gameplay},330)}
  };
})();
