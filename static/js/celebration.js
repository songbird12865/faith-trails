(function () {
  const overlay = document.getElementById('badge-overlay');
  if (!overlay) return;

  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  const badgeCircle = document.getElementById('badge-circle');
  const titleText = document.getElementById('badge-title');
  const subText = document.getElementById('badge-subtext');
  const continueBtn = document.getElementById('badge-continue-btn');
  const sound = document.getElementById('badge-sound');

  let particles = [];
  let rafId = null;
  let running = false;

  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function makeParticle() {
    const colors = ['#EF9F27', '#1D9E75', '#D85A30', '#7F77DD', '#378ADD'];
    return {
      x: Math.random() * canvas.width,
      y: -20,
      size: 5 + Math.random() * 5,
      speed: 1.5 + Math.random() * 2.5,
      drift: (Math.random() - 0.5) * 1.5,
      rotation: Math.random() * 360,
      spin: (Math.random() - 0.5) * 8,
      color: colors[Math.floor(Math.random() * colors.length)]
    };
  }

  function initParticles() {
    particles = [];
    for (let i = 0; i < 80; i++) {
      const p = makeParticle();
      p.y = Math.random() * canvas.height;
      particles.push(p);
    }
  }

  function animateConfetti() {
    if (!running) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const p of particles) {
      p.y += p.speed;
      p.x += p.drift;
      p.rotation += p.spin;
      if (p.y > canvas.height + 20) {
        Object.assign(p, makeParticle());
      }
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
      ctx.restore();
    }
    rafId = requestAnimationFrame(animateConfetti);
  }

  function playSound() {
    if (!sound) return;
    // Browsers block autoplay with sound until a user gesture has occurred
    // on the page. Since this fires right after a quiz/quest action (a click
    // or tap), it should be allowed. The catch() below silently ignores it
    // if the browser blocks it anyway, so it never breaks the page.
    sound.currentTime = 0;
    sound.play().catch(() => {});
  }

  function openCelebration() {
    overlay.classList.add('is-open');
    resizeCanvas();
    initParticles();
    running = true;
    animateConfetti();
    playSound();

    if (window.FaithTrailsAudio) {
      window.FaithTrailsAudio.switchToCelebration();
    }

    requestAnimationFrame(() => {
      badgeCircle.style.transition = 'transform 0.6s cubic-bezier(0.34,1.56,0.64,1)';
      badgeCircle.style.transform = 'scale(1)';
    });

    setTimeout(() => {
      titleText.style.transition = 'opacity 0.4s ease';
      titleText.style.opacity = '1';
    }, 300);
    setTimeout(() => {
      subText.style.transition = 'opacity 0.4s ease';
      subText.style.opacity = '1';
    }, 500);
    setTimeout(() => {
      continueBtn.style.transition = 'opacity 0.4s ease';
      continueBtn.style.opacity = '1';
    }, 700);
  }

  function closeCelebration() {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
    overlay.classList.remove('is-open');

    if (window.FaithTrailsAudio) {
      window.FaithTrailsAudio.switchToGameplay();
    }

    const redirect = continueBtn.getAttribute('data-redirect');
    if (redirect && redirect !== '#') {
      window.location.href = redirect;
    }
  }

  continueBtn.addEventListener('click', closeCelebration);
  window.addEventListener('resize', () => {
    if (running) resizeCanvas();
  });

  // Auto-open as soon as this partial loads, since it's only included
  // on pages where a badge was just earned.
  document.addEventListener('DOMContentLoaded', openCelebration);
  if (document.readyState !== 'loading') {
    openCelebration();
  }
})();
