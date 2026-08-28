(() => {
  // Player-related screens stay inside the current document so mobile browsers
  // keep the AudioContext that was unlocked by the original Start Adventure tap.
  // This prevents the audio gate from reappearing while changing/adding players.

  async function fetchDocument(url, options = {}) {
    const response = await fetch(url, {
      credentials: 'same-origin',
      ...options,
    });
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    const html = await response.text();
    return {
      response,
      doc: new DOMParser().parseFromString(html, 'text/html'),
    };
  }

  function updatePlayerStatus(doc) {
    const current = document.getElementById('player-status-slot');
    const incoming = doc.getElementById('player-status-slot');
    if (current && incoming) current.innerHTML = incoming.innerHTML;
  }

  async function activateGameIfPresent(doc, fallbackUrl) {
    const gameScript = doc.querySelector('script[src*="game.js"]');
    if (!gameScript) return;

    if (window.FaithTrailsGame &&
        typeof window.FaithTrailsGame.init === 'function') {
      window.FaithTrailsGame.init();
      return;
    }

    const src = gameScript.getAttribute('src');
    if (!src) return;

    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.body.appendChild(script);
    }).catch(() => {
      window.location.href = fallbackUrl;
    });
  }

  async function showPage(url, { replaceHistory = false } = {}) {
    const { response, doc } = await fetchDocument(url);
    const incomingMain = doc.getElementById('app-main');
    const currentMain = document.getElementById('app-main');
    if (!incomingMain || !currentMain) throw new Error('Missing #app-main');

    // Only replace player-specific header content. The music button and other
    // persistent controls stay in the DOM, so audio-engine.js keeps its bindings.
    updatePlayerStatus(doc);

    currentMain.innerHTML = incomingMain.innerHTML;
    document.title = doc.title;

    if (replaceHistory) history.replaceState({}, '', response.url);
    else history.pushState({}, '', response.url);

    window.scrollTo({ top: 0, behavior: 'auto' });
    await activateGameIfPresent(doc, response.url);
  }

  async function handlePlayerLink(link, options = {}) {
    const url = link.getAttribute('href');
    if (!url) return;
    try {
      await showPage(url, options);
    } catch (err) {
      // Navigation still works if an unexpected fetch/parsing problem occurs.
      window.location.href = url;
    }
  }

  document.addEventListener('click', async (event) => {
    const changePlayer = event.target.closest('[data-change-player]');
    if (changePlayer) {
      event.preventDefault();
      await handlePlayerLink(changePlayer);
      return;
    }

    const existingPlayer = event.target.closest('[data-player-select]');
    if (existingPlayer) {
      event.preventDefault();
      await handlePlayerLink(existingPlayer);
      return;
    }

    const newPlayer = event.target.closest('[data-new-player]');
    if (newPlayer) {
      event.preventDefault();
      await handlePlayerLink(newPlayer);
      return;
    }

    const difficultyButton = event.target.closest(
      '#create-profile-form .difficulty-option'
    );
    if (difficultyButton) {
      const form = difficultyButton.closest('#create-profile-form');
      if (!form) return;

      form.dataset.selectedDifficulty = difficultyButton.dataset.difficulty || '';
      form.querySelectorAll('.difficulty-option').forEach((button) => {
        button.classList.remove(
          'bg-trailgreen', 'text-parchment', 'border-trailgreen'
        );
        button.classList.add('bg-white');
      });
      difficultyButton.classList.remove('bg-white');
      difficultyButton.classList.add(
        'bg-trailgreen', 'text-parchment', 'border-trailgreen'
      );
    }
  });

  document.addEventListener('submit', async (event) => {
    const form = event.target.closest('#create-profile-form');
    if (!form) return;

    event.preventDefault();

    const input = form.querySelector('#name-input');
    const feedback = document.getElementById('create-feedback');
    const name = input?.value.trim() || '';
    const difficulty = form.dataset.selectedDifficulty || '';

    if (!name) {
      if (feedback) feedback.textContent = 'Please type a name first!';
      return;
    }
    if (!difficulty) {
      if (feedback) feedback.textContent = 'Please pick a difficulty level first!';
      return;
    }

    try {
      const response = await fetch('/api/profile', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, difficulty }),
      });

      const data = await response.json();
      if (!response.ok || !data.success) {
        if (feedback) {
          feedback.textContent =
            data.error || 'Something went wrong — please try again.';
        }
        return;
      }

      // Profile creation already established the Flask session. Fetch the map
      // into this same document instead of navigating/rebuilding the page.
      await showPage('/');
    } catch (err) {
      if (feedback) feedback.textContent = 'Something went wrong — please try again.';
    }
  });
})();
