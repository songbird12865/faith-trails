/*
  background_music.js

  Handles two looping tracks:
    - gameplay music: plays on every normal page (base template)
    - celebration music: plays only on the badge celebration screen

  MOBILE AUTOPLAY STRATEGY:
  Browsers will not allow audible autoplay before the user has interacted
  with the page. To get music started as close to "on landing" as possible
  (matching the feel of a native app), we:
    1. Start the track MUTED the instant the page loads (muted autoplay is
       allowed almost everywhere, so this succeeds reliably and the track
       is already playing/buffered).
    2. Unmute on the very first tap/click anywhere on the page. Because
       the audio is already running, unmuting is instant -- there's no
       "loading" delay, so it reads as if the music was already going.

  DUCKING:
  duck()/unduck() operate on whichever track is actually audible right now
  (gameplay OR celebration), not a hardcoded track. This matters because
  narration can play during either screen, and ducking the wrong (paused)
  track is a silent no-op that leaves the real music at full volume.

  USAGE:
  1. Include this script in your base.html template.
  2. Add <audio id="gameplay-music" loop muted> to base.html.
  3. Add <audio id="celebration-music" loop muted> to badge_celebration.html.
  4. Call FaithTrailsAudio.duck() before narration starts, and
     FaithTrailsAudio.unduck() when it stops/ends.
  5. celebration.js calls FaithTrailsAudio.switchToCelebration() when the
     badge screen opens, and FaithTrailsAudio.switchToGameplay() on Continue.
*/

window.FaithTrailsAudio = (function () {
  const GAMEPLAY_VOLUME = 0.35;
  const CELEBRATION_VOLUME = 0.4;
  const DUCK_VOLUME = 0.06;
  const STORAGE_KEY_MUTED = 'ft_music_muted';
  const STORAGE_KEY_UNLOCKED = 'ft_audio_unlocked';

  let duckedEl = null; // whichever <audio> element is currently ducked, if any

  function getGameplayEl() {
    return document.getElementById('gameplay-music');
  }
  function getCelebrationEl() {
    return document.getElementById('celebration-music');
  }

  // Whichever track is actually playing right now is the "active" one.
  function getActiveEl() {
    const cel = getCelebrationEl();
    if (cel && !cel.paused) return cel;
    const gp = getGameplayEl();
    if (gp && !gp.paused) return gp;
    return null;
  }

  function baseVolumeFor(el) {
    if (el === getCelebrationEl()) return CELEBRATION_VOLUME;
    return GAMEPLAY_VOLUME;
  }

  function isMuted() {
    return sessionStorage.getItem(STORAGE_KEY_MUTED) === '1';
  }

  function isUnlocked() {
    return sessionStorage.getItem(STORAGE_KEY_UNLOCKED) === '1';
  }

  function setMuted(muted) {
    sessionStorage.setItem(STORAGE_KEY_MUTED, muted ? '1' : '0');
    const gp = getGameplayEl();
    const cel = getCelebrationEl();
    // Respect the "unlocked" gate: never force muted=false here unless
    // the user has already interacted this session.
    if (gp) gp.muted = muted || !isUnlocked();
    if (cel) cel.muted = muted || !isUnlocked();
  }

  function startGameplay() {
    const gp = getGameplayEl();
    if (!gp) return;
    gp.volume = GAMEPLAY_VOLUME;
    // Always attempt playback muted first -- this succeeds reliably even
    // without a fresh user gesture, which is what keeps music consistent
    // across page navigations.
    gp.muted = true;
    gp.play().catch(() => {});
    sessionStorage.setItem('ft_music_started', '1');
    applyUnlockedState(gp);
  }

  // If the user already unlocked audio earlier this session (tapped
  // anywhere once), immediately unmute so subsequent pages don't need
  // a second tap.
  function applyUnlockedState(el) {
    if (!el) return;
    if (isUnlocked() && !isMuted()) {
      el.muted = false;
    }
  }

  // Called automatically on every normal page load (from base.html), so
  // music keeps playing across navigation once it's been started once.
  function resumeGameplayIfStarted() {
    if (sessionStorage.getItem('ft_music_started') === '1') {
      startGameplay();
    }
  }

  function switchToCelebration() {
    const gp = getGameplayEl();
    const cel = getCelebrationEl();
    if (gp) gp.pause();
    if (cel) {
      cel.volume = CELEBRATION_VOLUME;
      cel.muted = isMuted() || !isUnlocked();
      cel.currentTime = 0;
      cel.play().catch(() => {});
      applyUnlockedState(cel);
    }
  }

  function switchToGameplay() {
    const cel = getCelebrationEl();
    if (cel) cel.pause();
    startGameplay();
  }

  function toggleMute() {
    setMuted(!isMuted());
  }

  // Lower whichever track is currently playing, for narration.
  function duck() {
    const el = getActiveEl();
    if (!el) return;
    duckedEl = el;
    el.volume = DUCK_VOLUME;
  }

  // Restore whichever track was last ducked back to its normal volume.
  function unduck() {
    if (!duckedEl) return;
    duckedEl.volume = baseVolumeFor(duckedEl);
    duckedEl = null;
  }

  function unlockAudio() {
    if (isUnlocked()) return;
    sessionStorage.setItem(STORAGE_KEY_UNLOCKED, '1');
    if (isMuted()) return;
    const active = getActiveEl() || getGameplayEl();
    if (active) active.muted = false;
  }

  return {
    startGameplay,
    resumeGameplayIfStarted,
    switchToCelebration,
    switchToGameplay,
    toggleMute,
    isMuted,
    duck,
    unduck,
    unlockAudio
  };
})();

document.addEventListener('DOMContentLoaded', function () {
  // Start (muted) immediately on the very first page too, not just once
  // a "Start" button has been clicked, so it's already running by the
  // time the user's first tap unlocks sound.
  if (sessionStorage.getItem('ft_music_started') !== '1') {
    window.FaithTrailsAudio.startGameplay();
  } else {
    window.FaithTrailsAudio.resumeGameplayIfStarted();
  }

  // The very first tap/pointerdown anywhere unlocks audio for the rest
  // of the session. pointerdown fires slightly before click on touch
  // devices, which shaves a little more perceived latency off.
  document.addEventListener('pointerdown', function unlockOnFirstTap() {
    window.FaithTrailsAudio.unlockAudio();
    document.removeEventListener('pointerdown', unlockOnFirstTap);
  }, { once: true });
});
