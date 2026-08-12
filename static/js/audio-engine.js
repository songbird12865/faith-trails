(() => {
  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  const gameplaySrc=gameplay.querySelector('source')?.src||gameplay.src;
  const celebrationSrc=celebration.querySelector('source')?.src||celebration.src;
  let active=gameplay, mode='gameplay', savedGameplayTime=0;
  let muted=localStorage.getItem('ft-muted')==='1';
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
    celebration.pause();celebration.currentTime=0;
    gameplay.volume=0;gameplay.muted=muted;
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
  }
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio={
    duck(){fade(active,.025,180)},unduck(){fade(active,mode==='celebration'?.40:.32,450)},
    celebrate(){
      if(!gameplay||mode==='celebration')return;
      savedGameplayTime=gameplay.currentTime||0;
      celebration.pause();celebration.currentTime=0;
      mode='celebration';
      gameplay.pause();gameplay.src=celebrationSrc;gameplay.load();
      gameplay.currentTime=0;gameplay.volume=0;gameplay.muted=muted;
      gameplay.play().then(()=>fade(gameplay,.40,650)).catch(()=>{});
      active=gameplay;
    },
    gameplay(){
      if(!gameplay||mode==='gameplay')return;
      celebration.pause();celebration.currentTime=0;
      mode='gameplay';
      gameplay.pause();gameplay.src=gameplaySrc;gameplay.load();
      gameplay.addEventListener('loadedmetadata',()=>{
        gameplay.currentTime=Math.min(savedGameplayTime,Math.max(0,gameplay.duration-.25));
      },{once:true});
      gameplay.volume=0;gameplay.muted=muted;
      gameplay.play().then(()=>fade(gameplay,.32,650)).catch(()=>{});
      active=gameplay;
    }
  };
})();
