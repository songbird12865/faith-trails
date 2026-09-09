(() => 
{
  // This module keeps all music and narration controls in one place.
  // Find the audio and control elements created by base.html.

  const gameplay=document.getElementById('gameplay-music');
  const celebration=document.getElementById('celebration-music');
  const gate=document.getElementById('audio-gate');
  const start=document.getElementById('start-adventure');
  const toggle=document.getElementById('music-toggle');
  const gameplaySrc=gameplay.querySelector('source')?.src||gameplay.src;
  const celebrationSrc=celebration.querySelector('source')?.src||celebration.src;

  // Track the active music mode, saved position, and mute setting.
  let active=gameplay, mode='gameplay', savedGameplayTime=0;
  let muted=localStorage.getItem('ft-muted')==='1';
  let audioContext=null, musicGain=null, musicSource=null;
  const fadeGeneration=new WeakMap();

  // Stop an older fade when a newer fade starts on the same audio element.
  const fade=(el,to,ms=500)=>
    {
    if (!el)return;
    const generation=(fadeGeneration.get(el)||0)+1;
    fadeGeneration.set(el,generation);
    const from=el.volume,at=performance.now();
    const tick=n=>{
      if (fadeGeneration.get(el)!==generation)return;
      const p=Math.min(1,(n-at)/ms);
      el.volume=from+(to-from)*p;
      if (p<1)requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  async function ensureAudioGraph()
  {
    // Create or resume the browser audio system after the player's first tap.
    const AudioContextClass=window.AudioContext||window.webkitAudioContext;
    if(!AudioContextClass)return false;
    try
    {
      if (!audioContext)
        {
        audioContext=new AudioContextClass();
        musicSource=audioContext.createMediaElementSource(gameplay);
        musicGain=audioContext.createGain();
        musicGain.gain.value=0;
        musicSource.connect(musicGain).connect(audioContext.destination);
        gameplay.volume=1;
        }
      if (audioContext.state!=='running')await audioContext.resume();
      return audioContext.state==='running';
    // Return false if the browser cannot create or resume the audio system.
    }
    catch(e){return false}
  }

  // Change the music volume immediately or through a short fade.
  function setMusicLevel(level,ms=0)
  {
    // Use Web Audio when available and regular element volume as a backup.
    if (musicGain&&audioContext)
      {
      const now=audioContext.currentTime;
      musicGain.gain.cancelScheduledValues(now);
      musicGain.gain.setValueAtTime(musicGain.gain.value,now);
      if(ms>0)musicGain.gain.linearRampToValueAtTime(level,now+ms/1000);
      else musicGain.gain.setValueAtTime(level,now);
      return;
      }
    fade(gameplay,level,ms||1);
  }
  // Keep the music button icon and accessible label current.
  function syncToggle(){if(toggle){toggle.textContent=muted?'♪':'♫';toggle.setAttribute('aria-label',muted?'Turn music on':'Turn music off')}}
  
  // Start the game music after the browser grants audio permission.
  async function unlock()
  {
    // Reset celebration music so two tracks cannot play together.
    celebration.pause();celebration.currentTime=0;
    const graphReady=await ensureAudioGraph();
    if(!graphReady)
      {
      sessionStorage.removeItem('ft-audio-unlocked');
      gate?.classList.remove('is-hidden');
      return;
      }
    setMusicLevel(0);gameplay.muted=muted;
    try
    {
      await gameplay.play();
    }catch(e)
    {
      // Keep the start screen visible when the browser still blocks audio.
      sessionStorage.removeItem('ft-audio-unlocked');
      gate?.classList.remove('is-hidden');
      return;
    }
    gate?.classList.add('is-hidden');
    sessionStorage.setItem('ft-audio-unlocked','1');
    active=gameplay;
    setMusicLevel(.25,700);
  }
  // Restore audio during the same browser session when permission still works.
  if(sessionStorage.getItem('ft-audio-unlocked')==='1') unlock();

  // Connect the start and mute buttons to their actions.
  start?.addEventListener('click',unlock);
  toggle?.addEventListener('click',()=>{muted=!muted;localStorage.setItem('ft-muted',muted?'1':'0');gameplay.muted=celebration.muted=muted;syncToggle()});syncToggle();
  window.FaithTrailsAudio=
  {
    // Lower the music for narration and restore it when narration ends.
    duck(){setMusicLevel(.008,140)},unduck(){setMusicLevel(mode==='celebration'?.34:.25,500)},
    celebrate()
    {
      // Switch the authorized audio element to the celebration song.
      if(!gameplay||mode==='celebration')return;
      savedGameplayTime=gameplay.currentTime||0;
      celebration.pause();celebration.currentTime=0;
      mode='celebration';
      gameplay.pause();gameplay.src=celebrationSrc;gameplay.load();
      gameplay.currentTime=0;setMusicLevel(0);gameplay.muted=muted;
      gameplay.play().then(()=>setMusicLevel(.34,650)).catch(()=>{});
      active=gameplay;
    },
    gameplay()
    {
      // Switch back to gameplay music at its previously saved position.
      if(!gameplay||mode==='gameplay')return;
      celebration.pause();celebration.currentTime=0;
      mode='gameplay';
      gameplay.pause();gameplay.src=gameplaySrc;gameplay.load();
      gameplay.addEventListener('loadedmetadata',()=>
        {
        gameplay.currentTime=Math.min(savedGameplayTime,Math.max(0,gameplay.duration-.25));
        },{once:true});
      setMusicLevel(0);gameplay.muted=muted;
      gameplay.play().then(()=>setMusicLevel(.25,650)).catch(()=>{});
      active=gameplay;
    }
  };
})();
