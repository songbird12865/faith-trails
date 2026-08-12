(() => {
  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  let active=gameplay, muted=localStorage.getItem('ft-muted')==='1';
  const fade=(el,to,ms=500)=>{const from=el.volume,at=performance.now();const tick=n=>{const p=Math.min(1,(n-at)/ms);el.volume=from+(to-from)*p;if(p<1)requestAnimationFrame(tick)};requestAnimationFrame(tick)};
  function syncToggle(){if(toggle){toggle.textContent=muted?'♪':'♫';toggle.setAttribute('aria-label',muted?'Turn music on':'Turn music off')}}
  async function unlock(){
    gate?.classList.add('is-hidden');
    sessionStorage.setItem('ft-audio-unlocked','1');
    gameplay.volume=0;gameplay.muted=muted;
    celebration.volume=0;celebration.muted=true;
    // Unlock both independent audio players during the child's actual tap.
    // Safari/iOS may otherwise reject the celebration track when it starts
    // later, after an asynchronous badge-save request has finished.
    try{
      await Promise.all([gameplay.play(),celebration.play()]);
      celebration.pause();celebration.currentTime=0;celebration.muted=muted;
      fade(gameplay,.32,700);
    }catch(e){
      celebration.pause();celebration.currentTime=0;celebration.muted=muted;
      gameplay.play().then(()=>fade(gameplay,.32,700)).catch(()=>{});
    }
  }
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio={
    duck(){fade(active,.06,250)},unduck(){fade(active,active===celebration?.40:.32,350)},
    celebrate(){if(!celebration)return;celebration.currentTime=0;celebration.volume=0;celebration.muted=muted;celebration.play().then(()=>fade(celebration,.4,650)).catch(()=>{});fade(gameplay,0,400);setTimeout(()=>gameplay.pause(),420);active=celebration},
    gameplay(){if(!gameplay)return;fade(celebration,0,350);setTimeout(()=>{celebration.pause();gameplay.volume=0;gameplay.muted=muted;gameplay.play().catch(()=>{});fade(gameplay,.32,650);active=gameplay},330)}
  };
})();
