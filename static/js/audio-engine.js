(() => {
  const gameplay = document.getElementById('gameplay-music');
  const celebration = document.getElementById('celebration-music');
  const gate = document.getElementById('audio-gate');
  const start = document.getElementById('start-adventure');
  const toggle = document.getElementById('music-toggle');
  if (!gameplay || !celebration) return;
  const gameplaySrc = gameplay.querySelector('source')?.src || gameplay.src;
  const celebrationSrc = celebration.querySelector('source')?.src || celebration.src;
  let mode = 'gameplay', savedGameplayTime = 0;
  let muted = localStorage.getItem('ft-muted') === '1';
  let ducked = false, unlocked = false, generation = 0;
  let audioContext = null, musicGain = null;
  let restorePosition = null;
  const fadeGeneration = new WeakMap();

  function cancelFade(el) {
    fadeGeneration.set(el, (fadeGeneration.get(el) || 0) + 1);
  }
  function setMusicLevel(level, ms = 0) {
    // Off always wins, including during narration and delayed play callbacks.
    if (muted) { level = 0; ms = 0; }
    if (musicGain && audioContext) {
      const now = audioContext.currentTime;
      musicGain.gain.cancelScheduledValues(now);
      musicGain.gain.setValueAtTime(musicGain.gain.value, now);
      if (ms > 0) musicGain.gain.linearRampToValueAtTime(level, now + ms / 1000);
      else musicGain.gain.setValueAtTime(level, now);
      return;
    }
    cancelFade(gameplay);
    if (!ms) { gameplay.volume = level; return; }
    const ticket = fadeGeneration.get(gameplay);
    const from = gameplay.volume, at = performance.now();
    function tick(now) {
      if (fadeGeneration.get(gameplay) !== ticket) return;
      const p = Math.min(1, (now - at) / ms);
      gameplay.volume = from + (level - from) * p;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  const desiredLevel = () => ducked ? .008 : mode === 'celebration' ? .34 : .25;
  function silence() {
    gameplay.muted = celebration.muted = true;
    gameplay.pause();
    celebration.pause();
    cancelFade(gameplay);
    setMusicLevel(0);
  }
  function syncToggle() {
    if (!toggle) return;
    toggle.textContent = muted ? '♪' : '♫';
    toggle.setAttribute('aria-label', muted ? 'Turn music on' : 'Turn music off');
  }
  async function ensureAudioGraph() {
    const Context = window.AudioContext || window.webkitAudioContext;
    if (!Context) return false;
    try {
      if (!audioContext) {
        audioContext = new Context();
        const source = audioContext.createMediaElementSource(gameplay);
        musicGain = audioContext.createGain();
        musicGain.gain.value = 0;
        source.connect(musicGain).connect(audioContext.destination);
        gameplay.volume = 1;
      }
      if (audioContext.state !== 'running') await audioContext.resume();
      return audioContext.state === 'running';
    } catch (_) { return false; }
  }
  async function playCurrent() {
    const ticket = ++generation;
    celebration.pause();
    celebration.muted = true; // Only gameplay is routed through the music gain.
    if (muted) { silence(); return true; }
    if (!unlocked) return false;
    const ready = await ensureAudioGraph();
    if (ticket !== generation || muted || !unlocked) return false;
    if (!ready) return false;
    setMusicLevel(0);
    gameplay.muted = false;
    try { await gameplay.play(); }
    catch (_) { return false; }
    if (ticket !== generation || muted || !unlocked) {
      if (muted || !unlocked) silence();
      return false;
    }
    setMusicLevel(desiredLevel(), 650);
    return true;
  }
  async function unlock() {
    unlocked = true;
    const ok = await playCurrent();
    if (!ok && !muted) {
      sessionStorage.removeItem('ft-audio-unlocked');
      gate?.classList.remove('is-hidden');
      return;
    }
    gate?.classList.add('is-hidden');
    sessionStorage.setItem('ft-audio-unlocked', '1');
  }
  function switchMode(next) {
    if (mode === next) return;
    ++generation;
    if (mode === 'gameplay') savedGameplayTime = gameplay.currentTime || 0;
    if (restorePosition) {
      gameplay.removeEventListener('loadedmetadata', restorePosition);
      restorePosition = null;
    }
    silence();
    mode = next;
    gameplay.src = next === 'celebration' ? celebrationSrc : gameplaySrc;
    if (next === 'gameplay') {
      restorePosition = () => {
        const duration = gameplay.duration;
        gameplay.currentTime = Number.isFinite(duration)
          ? Math.min(savedGameplayTime, Math.max(0, duration - .25)) : savedGameplayTime;
        restorePosition = null;
      };
      gameplay.addEventListener('loadedmetadata', restorePosition, {once: true});
    }
    gameplay.load();
    if (!muted && unlocked) void playCurrent();
  }
  // Guard against a pending native play event arriving after Off was selected.
  gameplay.addEventListener('play', () => { if (muted) silence(); });
  celebration.addEventListener('play', () => celebration.pause());
  toggle?.addEventListener('click', () => {
    muted = !muted;
    ++generation;
    localStorage.setItem('ft-muted', muted ? '1' : '0');
    syncToggle();
    if (muted) silence();
    else void unlock();
  });
  start?.addEventListener('click', unlock);
  window.FaithTrailsAudio = {
    duck() { ducked = true; setMusicLevel(desiredLevel(), 140); },
    unduck() { ducked = false; setMusicLevel(desiredLevel(), 500); },
    celebrate() { switchMode('celebration'); },
    gameplay() { switchMode('gameplay'); }
  };
  silence();
  syncToggle();
  if (sessionStorage.getItem('ft-audio-unlocked') === '1') void unlock();
})();
