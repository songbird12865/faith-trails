/*
  background_music.js

  Handles two looping tracks:
    - gameplay music: plays on every normal page (base template)
    - celebration music: plays only on the badge celebration screen

  USAGE:
  1. Include this script in your base.html template (see snippet below).
  2. Add <audio id="gameplay-music" loop> to base.html.
  3. Add <audio id="celebration-music" loop> to badge_celebration.html.
  4. On your very first landing/start page, call FaithTrailsAudio.startGameplay()
     from the "Start" button's click handler (needed because browsers block
     autoplay with sound until the user has interacted with the page once).
  5. celebration.js (already provided) will call
     FaithTrailsAudio.switchToCelebration() when the badge screen opens,
     and FaithTrailsAudio.switchToGameplay() when "Continue" is clicked.
*/

window.FaithTrailsAudio = (function () {
  const GAMEPLAY_VOLUME = 0.4;
  const CELEBRATION_VOLUME = 0.5;
  const STORAGE_KEY_MUTED = 'ft_music_muted';

  function getGameplayEl() {
    return document.getElementById('gameplay-music');
  }
  function getCelebrationEl() {
    return document.getElementById('celebration-music');
  }

  function isMuted() {
    return sessionStorage.getItem(STORAGE_KEY_MUTED) === '1';
  }

  function setMuted(muted) {
    sessionStorage.setItem(STORAGE_KEY_MUTED, muted ? '1' : '0');
    const gp = getGameplayEl();
    const cel = getCelebrationEl();
    if (gp) gp.muted = muted;
    if (cel) cel.muted = muted;
  }

  function startGameplay() {
    const gp = getGameplayEl();
    if (!gp) return;
    gp.volume = GAMEPLAY_VOLUME;
    gp.muted = isMuted();
    gp.play().catch(() => {});
    sessionStorage.setItem('ft_music_started', '1');
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
      cel.muted = isMuted();
      cel.currentTime = 0;
      cel.play().catch(() => {});
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

  return {
    startGameplay,
    resumeGameplayIfStarted,
    switchToCelebration,
    switchToGameplay,
    toggleMute,
    isMuted
  };
})();

document.addEventListener('DOMContentLoaded', function () {
  window.FaithTrailsAudio.resumeGameplayIfStarted();

  // Fallback: some browsers block audio.play() when it's triggered
  // automatically on page load (not tied to a direct click), even if
  // music was already started earlier in this session. If that happens,
  // the gameplay track will be paused even though it should be playing.
  // This listener catches the very next click anywhere on the page and
  // uses it to resume the music, since a real click always satisfies
  // the browser's autoplay permission requirement.
  document.addEventListener('click', function resumeOnFirstClick() {
    const gp = document.getElementById('gameplay-music');
    const startedFlag = sessionStorage.getItem('ft_music_started') === '1';
    const celebrationOpen = document.getElementById('badge-overlay')
      && document.getElementById('badge-overlay').classList.contains('is-open');

    if (gp && startedFlag && gp.paused && !celebrationOpen) {
      gp.play().catch(() => {});
    }
    document.removeEventListener('click', resumeOnFirstClick);
  }, { once: true });
});
