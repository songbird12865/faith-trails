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
    return {
    
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
    const card = event.target.closest('[data-player-card]');
    if (card && event.target.closest('[data-player-rename]')) {
      const form = card.querySelector('[data-player-rename-form]');
      form.hidden = false;
      form.querySelector('input[name="name"]').focus();
      return;
    }
    if (card && event.target.closest('[data-player-rename-cancel]')) {
      card.querySelector('[data-player-rename-form]').hidden = true;
      return;
    }
if (card && event.target.closest('[data-player-delete]')) {
  event.preventDefault();

  const button = event.target.closest('[data-player-delete]');
  const controls = button.parentElement;
  const name = card.querySelector('[data-player-name]').textContent.trim();

  // Show an in-page confirmation instead of the browser's native confirm box.
  controls.innerHTML = '';

  const message = document.createElement('span');
  message.textContent = `Delete ${name}?`;
  message.className = 'font-bold text-red-700';

  const cancelButton = document.createElement('button');
  cancelButton.type = 'button';
  cancelButton.textContent = 'Cancel';
  cancelButton.className = 'font-bold text-slate-600 underline';

  const confirmButton = document.createElement('button');
  confirmButton.type = 'button';
  confirmButton.textContent = 'Delete';
  confirmButton.className = 'font-bold text-red-700 underline';

  controls.append(message, cancelButton, confirmButton);

  cancelButton.addEventListener('click', async () => {
    await showPage('/players', { replaceHistory: true });
  });

  confirmButton.addEventListener('click', async () => {
    confirmButton.disabled = true;

    try {
      const response = await fetch(`/api/players/${card.dataset.playerId}`, {
        method: 'DELETE',
        credentials: 'same-origin'
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || 'Could not delete player.');
      }

      await showPage('/players', { replaceHistory: true });
    } catch (error) {
      window.alert(error.message || 'Could not delete player. Please try again.');
      confirmButton.disabled = false;
    }
  });

  return;
}

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
    const renameForm = event.target.closest('[data-player-rename-form]');
    if (renameForm) {
      event.preventDefault();
      const card = renameForm.closest('[data-player-card]');
      const input = renameForm.querySelector('input[name="name"]');
      const feedback = renameForm.querySelector('[data-player-feedback]');
      const save = renameForm.querySelector('button[type="submit"]');
      save.disabled = true;
      feedback.hidden = true;
      try {
        const response = await fetch(`/api/players/${card.dataset.playerId}`, {
          method: 'PATCH', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: input.value.trim() })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Could not rename player.');
        await showPage('/players', { replaceHistory: true });
      } catch (error) {
        feedback.textContent = error.message || 'Could not rename player. Please try again.';
        feedback.hidden = false;
        save.disabled = false;
      }
      return;
    }

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
