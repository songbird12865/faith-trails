(() => {
  // Centralized audio controller. Keeping music and narration coordination in
  // one module prevents individual screens from starting competing tracks.
  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  const gameplaySrc=gameplay.querySelector('source')?.src||gameplay.src;
  const celebrationSrc=celebration.querySelector('source')?.src||celebration.src;
  let active=gameplay, mode='gameplay', savedGameplayTime=0;
  let muted=localStorage.getItem('ft-muted')==='1';
  let audioContext=null, musicGain=null, musicSource=null;
  const fadeGeneration=new WeakMap();
  // Each new fade invalidates the previous animation for the same element.
  // This avoids race conditions when a child changes screens during a fade.
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
  async function ensureAudioGraph(){
    // Mobile browsers require an AudioContext to be resumed by a user gesture.
    // The Start Adventure gate supplies that gesture before gameplay begins.
    const AudioContextClass=window.AudioContext||window.webkitAudioContext;
    if(!AudioContextClass)return false;
    try{
      if(!audioContext){
        audioContext=new AudioContextClass();
        musicSource=audioContext.createMediaElementSource(gameplay);
        musicGain=audioContext.createGain();
        musicGain.gain.value=0;
        musicSource.connect(musicGain).connect(audioContext.destination);
        gameplay.volume=1;
      }
      if(audioContext.state!=='running')await audioContext.resume();
      return audioContext.state==='running';
    }catch(e){return false}
  }
  function setMusicLevel(level,ms=0){
    // Prefer Web Audio gain ramps because they provide dependable narration
    // ducking; fall back to element volume when Web Audio is unavailable.
    if(musicGain&&audioContext){
      const now=audioContext.currentTime;
      musicGain.gain.cancelScheduledValues(now);
      musicGain.gain.setValueAtTime(musicGain.gain.value,now);
      if(ms>0)musicGain.gain.linearRampToValueAtTime(level,now+ms/1000);
      else musicGain.gain.setValueAtTime(level,now);
      return;
    }
    fade(gameplay,level,ms||1);
  }
  function syncToggle(){if(toggle){toggle.textContent=muted?'♪':'♫';toggle.setAttribute('aria-label',muted?'Turn music on':'Turn music off')}}
  async function unlock(){
    // Always reset the unused celebration element before unlocking gameplay so
    // a stale page state cannot leave both tracks playing.
    celebration.pause();celebration.currentTime=0;
    const graphReady=await ensureAudioGraph();
    if(!graphReady){
      sessionStorage.removeItem('ft-audio-unlocked');
      gate?.classList.remove('is-hidden');
      return;
    }
    setMusicLevel(0);gameplay.muted=muted;
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
    setMusicLevel(.25,700);
  }
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio={
    // Narration calls duck()/unduck() rather than manipulating music directly.
    duck(){setMusicLevel(.008,140)},unduck(){setMusicLevel(mode==='celebration'?.34:.25,500)},
    celebrate(){
      // Reuse the already-authorized gameplay element for the celebration
      // source. Some mobile browsers block a second audio element mid-session.
      if(!gameplay||mode==='celebration')return;
      savedGameplayTime=gameplay.currentTime||0;
      celebration.pause();celebration.currentTime=0;
      mode='celebration';
      gameplay.pause();gameplay.src=celebrationSrc;gameplay.load();
      gameplay.currentTime=0;setMusicLevel(0);gameplay.muted=muted;
      gameplay.play().then(()=>setMusicLevel(.34,650)).catch(()=>{});
      active=gameplay;
    },
    gameplay(){
      // Restore the position saved before celebration so the background theme
      // continues naturally instead of restarting after every badge.
      if(!gameplay||mode==='gameplay')return;
      celebration.pause();celebration.currentTime=0;
      mode='gameplay';
      gameplay.pause();gameplay.src=gameplaySrc;gameplay.load();
      gameplay.addEventListener('loadedmetadata',()=>{
        gameplay.currentTime=Math.min(savedGameplayTime,Math.max(0,gameplay.duration-.25));
      },{once:true});
      setMusicLevel(0);gameplay.muted=muted;
      gameplay.play().then(()=>setMusicLevel(.25,650)).catch(()=>{});
      active=gameplay;
    }
  };
})();
