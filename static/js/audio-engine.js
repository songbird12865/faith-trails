(() => {
  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  let active=gameplay, muted=localStorage.getItem('ft-muted')==='1';
  const fadeGeneration=new WeakMap();
  const fade=(el,to,ms=500)=>{
    if(!el)return;
    const generation=(fadeGeneration.get(el)||0)+1;
    fadeGeneration.set(el,generation);
    const from=el.volume,at=performance.now();
    const tick=n=>{
      if(fadeGeneration.get(el)!==generation)return;
      const p=Math.min(1,(n-at)/ms);
      el.volume=from+(to-from)*p;
      if(p<1)requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  function syncToggle(){if(toggle){toggle.textContent=muted?'♪':'♫';toggle.setAttribute('aria-label',muted?'Turn music on':'Turn music off')}}
  async function unlock(){
    gameplay.volume=0;gameplay.muted=muted;
    celebration.volume=0;celebration.muted=true;
    try{
      await gameplay.play();
    }catch(e){
      // A remembered session is not proof that a new mobile page has audio
      // permission. Keep the Start Adventure button visible so the child can
      // provide the tap required by iOS/Android browsers.
      sessionStorage.removeItem('ft-audio-unlocked');
      gate?.classList.remove('is-hidden');
      return;
    }
    gate?.classList.add('is-hidden');
    sessionStorage.setItem('ft-audio-unlocked','1');
    active=gameplay;
    fade(gameplay,.32,700);

    // Prime the separate celebration player during the same permitted tap.
    // Failure here does not stop the gameplay track.
    celebration.play().then(()=>{
      celebration.pause();celebration.currentTime=0;celebration.muted=muted;
    }).catch(()=>{celebration.pause();celebration.currentTime=0;celebration.muted=muted});
  }
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio={
    duck(){fade(active,.025,180)},unduck(){fade(active,active===celebration?.40:.32,450)},
    celebrate(){if(!celebration)return;celebration.currentTime=0;celebration.volume=0;celebration.muted=muted;celebration.play().then(()=>fade(celebration,.4,650)).catch(()=>{});fade(gameplay,0,400);setTimeout(()=>gameplay.pause(),420);active=celebration},
    gameplay(){if(!gameplay)return;fade(celebration,0,350);setTimeout(()=>{celebration.pause();gameplay.volume=0;gameplay.muted=muted;gameplay.play().catch(()=>{});fade(gameplay,.32,650);active=gameplay},330)}
  };
})();
