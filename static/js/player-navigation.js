(() => 
{
  // Keep player screens in the same page so music and audio permission continue.

  // Request another page and turn its HTML text into a document object.
  async function fetchDocument(url, options = {}) 
  {
    const response = await fetch(url, 
      {
      credentials: 'same-origin',
      ...options,
      }
  );
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    const html = await response.text();
    return 
    {
      response,
      doc: new DOMParser().parseFromString(html, 'text/html'),
    };
  }

  // Replace only the player name and player controls in the header.
  function updatePlayerStatus(doc) 
  {
    const current = document.getElementById('player-status-slot');
    const incoming = doc.getElementById('player-status-slot');
    if (current && incoming) current.innerHTML = incoming.innerHTML;
  }

  // Start game.js when the newly loaded page contains the game shell.
  async function activateGameIfPresent(doc, fallbackUrl) 
  {
    const gameScript = doc.querySelector('script[src*="game.js"]');
    if (!gameScript) return;

    // Reuse the game engine if it is already loaded in the browser.
    if (window.FaithTrailsGame &&
        typeof window.FaithTrailsGame.init === 'function') 
      {
      window.FaithTrailsGame.init();
      return;
      }

    const src = gameScript.getAttribute('src');
    if (!src) return;

    // Load game.js when this is the first game screen in the document.
    await new Promise((resolve, reject) => 
    {
      const script = document.createElement('script');
      script.src = src;
      script.onload = resolve;
      script.onerror = reject;
      document.body.appendChild(script);
    }
  )
  .catch(() => 
    {
      window.location.href = fallbackUrl;
    }
  );
  }

  // Place a requested player page inside the current document.
  async function showPage(url, { replaceHistory = false } = {}) 
  {
    const { response, doc } = await fetchDocument(url);
    const incomingMain = doc.getElementById('app-main');
    const currentMain = document.getElementById('app-main');
    if (!incomingMain || !currentMain) throw new Error('Missing #app-main');

    // Leave the music controls in place while updating the player information.
    updatePlayerStatus(doc);

    currentMain.innerHTML = incomingMain.innerHTML;
    document.title = doc.title;

    // Update browser history so Back and Forward still behave normally.
    if (replaceHistory) history.replaceState({}, '', response.url);
    else history.pushState({}, '', response.url);

    window.scrollTo({ top: 0, behavior: 'auto' });
    await activateGameIfPresent(doc, response.url);
  }

  // Use single-page navigation and fall back to a normal link if needed.
  async function handlePlayerLink(link, options = {}) 
  {
    const url = link.getAttribute('href');
    if (!url) return;
    try 
    {
      await showPage(url, options);
    } catch (err) {
      // Use regular navigation if the single-page request fails.
      window.location.href = url;
    }
  }

  // Handle player links and difficulty buttons with one click listener.
  document.addEventListener('click', async (event) => 
    {
    const changePlayer = event.target.closest('[data-change-player]');
    if (changePlayer) 
      {
      event.preventDefault();
      await handlePlayerLink(changePlayer);
      return;
      }

    const existingPlayer = event.target.closest('[data-player-select]');
    if (existingPlayer) 
      {
      event.preventDefault();
      await handlePlayerLink(existingPlayer);
      return;
      }

    const newPlayer = event.target.closest('[data-new-player]');
    if (newPlayer) 
      {
      event.preventDefault();
      await handlePlayerLink(newPlayer);
      return;
     }

    const difficultyButton = event.target.closest(
      '#create-profile-form .difficulty-option'
    );
    if (difficultyButton) 
      {
      const form = difficultyButton.closest('#create-profile-form');
      if (!form) return;

      // Save the selected level and update the button colors.
      form.dataset.selectedDifficulty = difficultyButton.dataset.difficulty || '';
      form.querySelectorAll('.difficulty-option').forEach((button) => 
        {
        button.classList.remove(
          'bg-trailgreen', 'text-parchment', 'border-trailgreen'
        );
        button.classList.add('bg-white');
        }
      );
      difficultyButton.classList.remove('bg-white');
      difficultyButton.classList.add(
        'bg-trailgreen', 'text-parchment', 'border-trailgreen'
      );
    }
  }
);

  // Validate and submit the New Player form without reloading the page.
  document.addEventListener('submit', async (event) => 
    {
    const form = event.target.closest('#create-profile-form');
    if (!form) return;

    event.preventDefault();

    const input = form.querySelector('#name-input');
    const feedback = document.getElementById('create-feedback');
    const name = input?.value.trim() || '';
    const difficulty = form.dataset.selectedDifficulty || '';

    // Stop submission until both required choices are provided.
    if (!name) 
      {
      if (feedback) feedback.textContent = 'Please type a name first!';
      return;
      }
    if (!difficulty) 
      {
      if (feedback) feedback.textContent = 'Please pick a difficulty level first!';
      return;
     }

    // Send the valid name and difficulty to Flask as JSON.
    try 
    {
      const response = await fetch('/api/profile', 
        {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, difficulty }),
        }
    );

      const data = await response.json();
      if (!response.ok || !data.success) 
        {
        if (feedback) 
          {
          feedback.textContent =
            data.error || 'Something went wrong — please try again.';
          }
        return;
        }

      // The new profile is logged in, so load its trail into this page.
      await showPage('/');
    // Give the player a simple message if the request cannot finish.
    } 
    catch (err) 
    {
      if (feedback) feedback.textContent = 'Something went wrong — please try again.';
    }
  }
);
})();
