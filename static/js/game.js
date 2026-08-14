(() => {
  // Flask embeds the signed-in profile, quest catalog, and earned badge IDs as
  // JSON. The single-page game shell uses this bootstrap data immediately and
  // requests fresh quest/progress details from the API when needed.
  const boot=JSON.parse(document.getElementById('game-bootstrap').textContent);
  const mapView=document.getElementById('map-view'),questView=document.getElementById('quest-view');
  const state={earned:new Set(boot.earned),quest:null,scenes:[],current:0,lesson:'',lessonNarration:null,narration:null,championKnown:false,championJustUnlocked:false};
  // Escape all server-provided or player-provided text before inserting it into
  // HTML templates. This prevents names and content from becoming executable.
  const esc=s=>String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  const img=slug=>`/static/img/quests/${slug}.jpg`;
  const button=(label,fn,kind='primary-button')=>{const b=document.createElement('button');b.className=kind;b.textContent=label;b.onclick=fn;return b};
  const toast=msg=>{const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)};

  function transition(from,to,render){from.classList.add('is-leaving');setTimeout(()=>{from.hidden=true;from.classList.remove('is-leaving');render();to.hidden=false;to.style.animation='none';void to.offsetWidth;to.style.animation='';scrollTo({top:0,behavior:'smooth'})},260)}

  // ----- Trail map and saved-progress views -----
  function renderMap(){
    history.replaceState({view:'map'},'', '/');
    mapView.innerHTML=`<div class="hero trail-map-heading"><div class="hero-kicker">${esc(boot.profile.current_difficulty)} adventure</div><h1>Your Faith Trail</h1><p>Follow the winding path, choose a Bible adventure, and collect every badge!</p><div class="choice-grid" id="difficulty-picker"></div></div><div class="faith-trail-map" id="faith-trail-map"><div class="trail-forest-glow" aria-hidden="true"></div><svg class="journey-svg" id="journey-svg" aria-hidden="true"><path id="journey-shadow"></path><path id="journey-line"></path></svg><div class="trail-stops">${boot.quests.map((q,i)=>`<div class="trail-stop trail-stop--${i%2?'right':'left'}" style="--stop-delay:${.45+i*.16}s"><button class="adventure-stop ${q.is_available?'':'locked'} ${state.earned.has(q.id)?'earned':''}" data-slug="${esc(q.slug)}" aria-label="${esc(q.title)}${q.is_available?'':' — coming soon'}"><span class="stop-ring"><img src="${img(q.slug)}" alt=""><span class="stop-number">${q.sort_order}</span>${state.earned.has(q.id)?'<span class="stop-earned" aria-label="Badge earned">✓</span>':''}${q.is_available?'':'<span class="stop-lock">🔒</span>'}</span><span class="stop-sign"><strong>${esc(q.title)}</strong><small>${esc(q.summary)}</small></span></button></div>`).join('')}</div><div class="trail-finish" aria-hidden="true">🏁</div></div>`;
    const picker=mapView.querySelector('#difficulty-picker');
    boot.difficulties.forEach(level=>{const b=button(level,()=>changeDifficulty(level),'game-choice');if(level===boot.profile.current_difficulty)b.classList.add('correct');picker.appendChild(b)});
    mapView.querySelectorAll('.adventure-stop').forEach(tile=>tile.onclick=()=>{const q=boot.quests.find(x=>x.slug===tile.dataset.slug);q.is_available?openQuest(q.slug):toast('This adventure is coming soon!')});
    // Wait for two paint cycles so the quest markers have measurable positions
    // before calculating the responsive SVG trail between them.
    requestAnimationFrame(()=>requestAnimationFrame(drawFaithTrail));
    fetch('/api/progress').then(r=>r.ok?r.json():null).then(data=>{if(data&&data.earned&&data.earned.length>=18){state.championKnown=true;const trail=mapView.querySelector('.faith-trail-map');trail?.classList.add('champion-golden');if(trail&&!trail.querySelector('.champion-map-button')){const b=button('🏆 Grand Champion Celebration',renderChampion,'primary-button champion-map-button');trail.appendChild(b)}drawFaithTrail();}}).catch(()=>{});
  }

  function drawFaithTrail(){
    // Build a curved SVG path through the actual on-screen marker centers.
    // Recalculating from DOM geometry keeps the path aligned at every viewport.
    const map=document.getElementById('faith-trail-map'),svg=document.getElementById('journey-svg');
    const line=document.getElementById('journey-line'),shadow=document.getElementById('journey-shadow');
    if(!map||!svg||!line||!shadow)return;
    const rect=map.getBoundingClientRect(),rings=[...map.querySelectorAll('.stop-ring')];if(rings.length<2)return;
    svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`);svg.setAttribute('width',rect.width);svg.setAttribute('height',rect.height);
    const points=rings.map(r=>{const b=r.getBoundingClientRect();return{x:b.left+b.width/2-rect.left,y:b.top+b.height/2-rect.top}});
    let d=`M ${points[0].x} ${Math.max(0,points[0].y-85)} Q ${points[0].x-55} ${points[0].y-40} ${points[0].x} ${points[0].y}`;
    for(let i=0;i<points.length-1;i++){const a=points[i],b=points[i+1],mid=(a.y+b.y)/2,dir=i%2?1:-1;d+=` C ${a.x+dir*65} ${mid-38}, ${b.x-dir*65} ${mid+38}, ${b.x} ${b.y}`;}
    const last=points[points.length-1];d+=` Q ${last.x+45} ${last.y+55} ${rect.width/2} ${Math.min(rect.height-15,last.y+95)}`;
    line.setAttribute('d',d);shadow.setAttribute('d',d);
    const length=line.getTotalLength();line.style.setProperty('--trail-length',length);line.style.strokeDasharray=length;line.style.strokeDashoffset=length;
    line.getBoundingClientRect();line.classList.remove('drawn');requestAnimationFrame(()=>line.classList.add('drawn'));
  }
  async function renderCollection(kind){
    // One progress response powers both views: the badge case filters to the
    // current level, while Hall of Fame summarizes all three difficulties.
    const r=await fetch('/api/progress');if(!r.ok)return toast('Progress could not be loaded.');const data=await r.json();
    const title=kind==='badges'?'My Badge Collection':'Hall of Fame';
    mapView.innerHTML=`<div class="hero"><div class="hero-kicker">${esc(boot.profile.name)}’s achievements</div><h1>${title}</h1><p>${kind==='badges'?'Every completed trail adds another badge to your collection.':'All 18 badges across Easy, Medium, and Hard adventures.'}</p><button id="collection-back" class="primary-button">← Back to Trail</button></div><div id="collection-content"></div>`;
    const content=mapView.querySelector('#collection-content');
    if(kind==='hall'){
      // Hall of Fame is a true 6 × 3 progress grid: one row per adventure and
      // one badge position for each difficulty. Keep this separate from the
      // large cards used by the current-difficulty "My Badges" collection.
      const levels=['easy','medium','hard'];
      const earnedKeys=new Set(data.earned.map(e=>`${e.quest_id}:${e.difficulty}`));
      const earnedCount=data.earned.filter(e=>levels.includes(e.difficulty)).length;
      content.innerHTML=`<section class="hof-board"><div class="hof-summary"><strong>${earnedCount} of 18 earned</strong><div class="hof-meter" role="progressbar" aria-label="Hall of Fame badges earned" aria-valuemin="0" aria-valuemax="18" aria-valuenow="${earnedCount}"><span style="width:${earnedCount/18*100}%"></span></div></div><div class="hof-table-wrap"><table class="hof-table"><thead><tr><th scope="col">Adventure</th>${levels.map(level=>`<th scope="col" class="hof-${level}">${level}</th>`).join('')}</tr></thead><tbody>${data.quests.filter(q=>q.is_available).map(q=>`<tr><th scope="row"><img src="${img(q.slug)}" alt=""><span>${esc(q.title)}</span></th>${levels.map(level=>{const earned=earnedKeys.has(`${q.id}:${level}`);return `<td><span class="hof-badge hof-badge--${level} ${earned?'is-earned':'is-waiting'}" aria-label="${esc(q.title)} ${level} badge ${earned?'earned':'not earned'}"><img src="${img(q.slug)}" alt="" aria-hidden="true"><span>${earned?'✓':'☆'}</span></span></td>`}).join('')}</tr>`).join('')}</tbody></table></div><div class="hof-legend"><span><i class="hof-dot hof-dot--easy"></i>Easy · Bronze</span><span><i class="hof-dot hof-dot--medium"></i>Medium · Silver</span><span><i class="hof-dot hof-dot--hard"></i>Hard · Gold</span></div></section>`;
    }else{
      content.className='map-grid';
      data.quests.filter(q=>q.is_available).forEach((q,i)=>{const levels=data.earned.filter(e=>e.quest_id===q.id).map(e=>e.difficulty);const earned=levels.includes(boot.profile.current_difficulty);const el=document.createElement('article');el.className='quest-tile';el.style.animationDelay=`${i*.08}s`;el.innerHTML=`${earned?'<span class="earned-check">✓</span>':''}<img src="${img(q.slug)}" alt=""><div class="tile-copy"><h2>${esc(q.title)}</h2><p>${earned?`${esc(boot.profile.current_difficulty)} badge earned`:'Complete this trail to earn it'}</p></div>`;content.appendChild(el)});
    }
    mapView.querySelector('#collection-back').onclick=renderMap;
  }
  async function changeDifficulty(level){if(level===boot.profile.current_difficulty)return;const r=await fetch('/api/profile',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({difficulty:level})});if(r.ok)location.reload();else toast('Could not change difficulty.')}

  // ----- Quest loading and scene dispatch -----
  async function openQuest(slug,push=true){
    questView.innerHTML='<div class="hero"><div class="scene-emoji">🧭</div><h1>Loading your adventure…</h1></div>';
    transition(mapView,questView,()=>{});
    const r=await fetch(`/api/quest/${slug}`);if(!r.ok){showMap();return toast('That quest could not be loaded.')}
    const data=await r.json();state.quest=data.quest;state.scenes=data.scenes;state.lesson=data.lesson;state.lessonNarration=data.lesson_narration_file;state.current=0;
    if(push)history.pushState({view:'quest',slug},'',`/quest/${slug}`);renderQuestShell();renderScene();
  }
  function renderQuestShell(){questView.innerHTML=`<article class="quest-stage"><img class="quest-art-backdrop" src="${img(state.quest.slug)}" alt=""><img class="quest-art" src="${img(state.quest.slug)}" alt="${esc(state.quest.title)}"><div class="quest-art-shade"></div><div class="quest-top"><button class="glass-button" id="map-back">← Trail Map</button><span class="difficulty-pill">${esc(boot.profile.current_difficulty)}</span></div><div class="scene-panel"><div class="progress-track"><div id="progress-fill" class="progress-fill"></div></div><div id="scene-content" class="scene-content"></div><div id="scene-controls" class="scene-controls"></div></div></article>`;questView.querySelector('#map-back').onclick=showMap}
  function showMap(){stopNarration();history.pushState({view:'map'},'', '/');transition(questView,mapView,renderMap)}
  function advance(){stopNarration();state.current++;renderScene()}
  function renderScene(){
    const content=document.getElementById('scene-content'),controls=document.getElementById('scene-controls');if(!content)return;
    content.innerHTML='';controls.innerHTML='';document.getElementById('progress-fill').style.width=`${Math.min(100,(state.current/(state.scenes.length||1))*100)}%`;
    if(state.current>=state.scenes.length)return completeQuest();
    const s=state.scenes[state.current];playNarration(s.narration_file,s._narration_text||s.text||s.prompt||s.verse);
    // Scene data controls the renderer, allowing new quests to reuse the same
    // front-end engine instead of requiring a separate page for each story.
    if(s.type==='story')renderStory(s,content,controls);else if(s.type==='quiz')renderQuiz(s,content);else if(s.type==='memory_verse')renderVerse(s,content,controls);else if(s.subtype==='matching')renderMatching(s,content,controls);else if(s.subtype==='color_picker')renderColors(s,content,controls);else if(s.subtype==='sequence')renderSequence(s,content,controls);
  }
  function renderStory(s,c,k){c.innerHTML=`<div class="scene-emoji">${s.emoji||'✨'}</div><h2 class="scene-title">${esc(state.quest.title)}</h2><p class="scene-text">${esc(s.text)}</p>`;k.appendChild(button('Continue →',advance))}
  function renderQuiz(s,c){c.innerHTML=`<div class="scene-emoji">🤔</div><h2 class="scene-title">Choose your answer</h2><p class="scene-text">${esc(s.prompt)}</p><div class="choice-grid"></div><p class="feedback"></p>`;const grid=c.querySelector('.choice-grid'),f=c.querySelector('.feedback');s.options.forEach((o,i)=>{const b=button(o,()=>{if(i===s.correct_index){b.classList.add('correct');f.className='feedback good';f.textContent='That’s right! ✨';setTimeout(advance,800)}else{b.classList.remove('wrong');void b.offsetWidth;b.classList.add('wrong');f.className='feedback retry';f.textContent='Almost—try another answer!'}},'game-choice');grid.appendChild(b)})}
  function renderMatching(s,c,k){let count=0;c.innerHTML=`<div class="scene-emoji">👐</div><h2 class="scene-title">${esc(s.prompt)}</h2><div class="drop-zone"><span>Tap an item to move it here</span></div><div class="item-tray"></div>`;const tray=c.querySelector('.item-tray'),zone=c.querySelector('.drop-zone');s.items.forEach(item=>{const b=button(`${item.emoji} ${item.label}`,()=>{if(b.disabled)return;b.disabled=true;b.style.opacity='.3';if(zone.querySelector('span'))zone.innerHTML='';const x=document.createElement('div');x.className='game-item flying';x.textContent=item.emoji;zone.appendChild(x);if(++count===s.items.length)k.appendChild(button('Great job! Continue →',advance))},'game-item');tray.appendChild(b)})}
  function renderColors(s,c,k){const colors=Array(s.target_count).fill(null);const draw=()=>{c.innerHTML=`<div class="scene-emoji">🎨</div><h2 class="scene-title">${esc(s.prompt)}</h2><div class="coat">${colors.map(x=>`<div class="coat-stripe" style="background:${x||'#efe6d0'}"></div>`).join('')}</div><div class="choice-grid palette"></div>`;s.palette.forEach(col=>{const b=button(col.name,()=>{const n=colors.indexOf(null);if(n<0)return;colors[n]=col.hex;draw();if(!colors.includes(null)){k.innerHTML='';k.appendChild(button('Beautiful! Continue →',advance))}},'game-choice');b.style.borderColor=col.hex;b.style.background=col.hex;b.style.color='#fff';c.querySelector('.palette').appendChild(b)})};draw()}
  function renderSequence(s,c,k){let tray=[...s.items].sort(()=>Math.random()-.5),built=[];const draw=()=>{c.innerHTML=`<div class="scene-emoji">🧩</div><h2 class="scene-title">${esc(s.prompt)}</h2><div class="assembly-line"></div><div class="item-tray"></div><p class="feedback"></p>`;built.forEach((x,i)=>c.querySelector('.assembly-line').appendChild(button(`${i+1}. ${x.emoji} ${x.label}`,()=>{built= built.filter(y=>y.id!==x.id);tray.push(x);draw()},'word-chip')));tray.forEach(x=>c.querySelector('.item-tray').appendChild(button(`${x.emoji} ${x.label}`,()=>{built.push(x);tray=tray.filter(y=>y.id!==x.id);draw();if(!tray.length)check()},'game-item')))};const check=()=>{const ok=built.every((x,i)=>x.id===s.items[i].id),f=c.querySelector('.feedback');f.textContent=ok?'Perfect order! ✨':'Not quite. Tap a placed item to move it back.';f.className=`feedback ${ok?'good':'retry'}`;if(ok)k.appendChild(button('Continue →',advance))};draw()}
  function renderVerse(s,c,k){
    // Preserve duplicate words by assigning each word a unique numeric ID;
    // comparing only word text would remove every matching occurrence at once.
    const words=s.verse.split(' ').map((word,id)=>({word,id}));let tray=[],built=[];
    const learn=()=>{c.innerHTML=`<div class="scene-emoji">📖</div><h2 class="scene-title">Memory Verse</h2><p class="scene-text">“${esc(s.verse)}”</p><p><strong>${esc(s.reference)}</strong></p>`;k.innerHTML='';k.appendChild(button('Build the verse →',build))};
    const build=()=>{stopNarration();tray=[...words].sort(()=>Math.random()-.5);built=[];draw()};
    const draw=()=>{c.innerHTML='<h2 class="scene-title">Tap the words in order</h2><p class="scene-text">The numbers show the sentence order. Tap a placed word to move it back.</p><div class="assembly-line"></div><div class="item-tray"></div><p class="feedback"></p>';built.forEach((x,i)=>c.querySelector('.assembly-line').appendChild(button(`${i+1}. ${x.word}`,()=>{built=built.filter(y=>y.id!==x.id);tray.push(x);draw()},'word-chip')));tray.forEach(x=>c.querySelector('.item-tray').appendChild(button(x.word,()=>{built.push(x);tray=tray.filter(y=>y.id!==x.id);draw();if(!tray.length)check()},'word-chip')))};
    // Ignore punctuation and repeated whitespace when checking the child's
    // reconstruction, because the learning goal is correct word order.
    const normalize=text=>text.toLowerCase().replace(/[^a-z0-9\s]/g,'').replace(/\s+/g,' ').trim();
    const check=()=>{const assembled=normalize(built.map(x=>x.word).join(' ')),expected=normalize(s.verse),ok=assembled===expected,f=c.querySelector('.feedback');f.textContent=ok?'You built it! ✨':'The words are all here, but their order is not quite right. Tap a word to move it back.';f.className=`feedback ${ok?'good':'retry'}`;if(ok){k.innerHTML='';k.appendChild(button('Choose its Bible reference →',reference))}};
    const reference=()=>{c.innerHTML='<div class="scene-emoji">📍</div><h2 class="scene-title">Where is this verse found?</h2><div class="choice-grid"></div><p class="feedback"></p>';[...s.reference_options].sort(()=>Math.random()-.5).forEach(x=>{c.querySelector('.choice-grid').appendChild(button(x,()=>{const f=c.querySelector('.feedback');if(x===s.reference){f.textContent='Correct! ✨';f.className='feedback good';setTimeout(advance,700)}else{f.textContent='Try another reference.';f.className='feedback retry'}},'game-choice'))})};
    learn();
  }
  function speakWithDevice(text){if(!text||!('speechSynthesis' in window))return;const u=new SpeechSynthesisUtterance(text);u.rate=.9;u.pitch=1.08;u.onstart=()=>window.FaithTrailsAudio?.duck();u.onend=()=>window.FaithTrailsAudio?.unduck();u.onerror=()=>window.FaithTrailsAudio?.unduck();state.narration=u;window.speechSynthesis.speak(u)}
  // Use cached narration when available; device speech is a graceful fallback
  // if an MP3 cannot load or the narration service is not configured.
  function playNarration(file,text){stopNarration();if(!file)return speakWithDevice(text);const a=new Audio(`/api/narration/${encodeURIComponent(file)}`);state.narration=a;let fallbackUsed=false;a.addEventListener('play',()=>window.FaithTrailsAudio?.duck());a.addEventListener('ended',()=>window.FaithTrailsAudio?.unduck());a.addEventListener('error',()=>{if(fallbackUsed)return;fallbackUsed=true;state.narration=null;speakWithDevice(text)});a.play().catch(()=>{if(!fallbackUsed){fallbackUsed=true;state.narration=null;speakWithDevice(text)}})}
  function stopNarration(){if(state.narration instanceof Audio)state.narration.pause();if('speechSynthesis' in window)window.speechSynthesis.cancel();state.narration=null;window.FaithTrailsAudio?.unduck()}
  async function completeQuest(){
    stopNarration();
    await fetch(`/api/complete/${state.quest.slug}`,{method:'POST'}).catch(()=>{});
    state.earned.add(state.quest.id);
    const progress=await fetch('/api/progress').then(r=>r.ok?r.json():null).catch(()=>null);
    // Champion status is based on persisted server data rather than local state,
    // so refreshing or switching devices cannot create a false unlock.
    const nowChampion=Boolean(progress&&progress.earned&&progress.earned.length>=18);
    state.championJustUnlocked=nowChampion&&!state.championKnown;
    state.championKnown=nowChampion;
    openCelebration();
  }
  function openCelebration(){const o=document.getElementById('badge-overlay'),continueButton=document.getElementById('celebration-continue');document.getElementById('celebration-badge').textContent=state.quest.icon||'🏅';document.getElementById('celebration-copy').textContent=`You earned the ${boot.profile.current_difficulty} ${state.quest.title} badge! ${state.lesson}`;continueButton.textContent=state.championJustUnlocked?'See Your Grand Celebration!':'Return to the Trail';o.classList.add('open');o.setAttribute('aria-hidden','false');window.FaithTrailsAudio?.celebrate();confetti()}
  document.getElementById('celebration-continue').onclick=()=>{const o=document.getElementById('badge-overlay');o.classList.remove('open');o.setAttribute('aria-hidden','true');if(state.championJustUnlocked){state.championJustUnlocked=false;transition(questView,mapView,renderChampion)}else{window.FaithTrailsAudio?.gameplay();showMap()}};

  function renderChampion(){
    // This reward is unlocked only after all six quests are completed at all
    // three difficulty levels (6 quests × 3 levels = 18 badges).
    history.replaceState({view:'champion'},'', '/');
    window.FaithTrailsAudio?.celebrate();
    mapView.innerHTML=`<section class="grand-champion-screen"><canvas id="grand-confetti"></canvas><div class="golden-trail-intro" id="golden-trail-intro"><p class="champion-kicker">ALL 18 BADGES EARNED</p><h1>Your Whole Faith Trail Is Turning Gold!</h1><svg viewBox="0 0 700 230" aria-hidden="true"><path id="grand-trail-shadow" d="M40 45 C170 5 190 100 335 55 S545 15 655 70 C565 125 440 90 340 150 S145 215 45 165"/><path id="grand-trail-line" d="M40 45 C170 5 190 100 335 55 S545 15 655 70 C565 125 440 90 340 150 S145 215 45 165"/></svg><div class="grand-mini-badges">${Array.from({length:18},(_,i)=>`<span style="--badge-delay:${.45+i*.08}s">${['🌧️','🧥','🌊','🪨','🐋','🦁'][i%6]}</span>`).join('')}</div></div><div class="champion-final-card" id="champion-final-card" hidden><div class="grand-trophy">🏆</div><p class="champion-kicker">YOU DID IT!</p><h1>Faith-Trails Champion</h1><h2>All 18 badges earned!</h2><p class="champion-inscription">You have learned that God is Faithful through every journey!</p><div class="champion-message"><button id="hear-champion" class="champion-sound-button">🔊 Hear Your Champion Message</button><p>You followed Noah, Joseph, Moses, David, Jonah, and Daniel through every adventure. Each one trusted God in a different way—and now you know that you can trust Him too.</p><blockquote>“Trust in the Lord with all your heart.”<br><strong>— Proverbs 3:5</strong></blockquote></div><p class="champion-traits">You showed courage like David, faithfulness like Daniel, obedience like Jonah, trust like Joseph, bravery like Moses, and perseverance like Noah.</p><div class="champion-actions"><button id="view-certificate" class="primary-button">📜 My Certificate</button><button id="design-badge" class="primary-button">🎨 Secret Badge Designer</button><button id="champion-home" class="primary-button champion-quiet">Return to My Golden Trail</button></div></div></section>`;
    setTimeout(()=>{const intro=document.getElementById('golden-trail-intro'),final=document.getElementById('champion-final-card');if(!intro||!final)return;intro.classList.add('leaving');setTimeout(()=>{intro.hidden=true;final.hidden=false;requestAnimationFrame(()=>final.classList.add('show'));championConfetti()},550)},3500);
    setTimeout(()=>{document.getElementById('hear-champion')?.addEventListener('click',()=>playNarration('faith-trails-champion__0aaea93170.mp3','You followed Noah, Joseph, Moses, David, Jonah, and Daniel through every adventure. Each one trusted God in a different way, and now you know that you can trust Him too.'));document.getElementById('view-certificate')?.addEventListener('click',renderCertificate);document.getElementById('design-badge')?.addEventListener('click',renderBadgeDesigner);document.getElementById('champion-home')?.addEventListener('click',()=>{window.FaithTrailsAudio?.gameplay();renderMap()})},4200);
  }

  function renderCertificate(){
    mapView.innerHTML=`<div class="certificate-toolbar"><button id="certificate-back" class="primary-button">← Celebration</button><button id="certificate-print" class="primary-button">🖨️ Print or Save as PDF</button></div><section class="faith-certificate"><div class="certificate-inner"><div class="certificate-compass">🧭</div><p class="certificate-small">Faith-Trails: A Closer Walk for Kids</p><h1>Certificate of Faith and Courage</h1><p>This proudly certifies that</p><div class="certificate-name">${esc(boot.profile.name)}</div><p>completed all 18 Faith-Trails challenges and became a</p><h2>Faith-Trails Champion</h2><div class="certificate-seal">🏆</div><p class="certificate-inscription">You have learned that God is Faithful through every journey!</p><blockquote>“Trust in the Lord with all your heart.” — Proverbs 3:5</blockquote></div></section>`;
    document.getElementById('certificate-back').onclick=renderChampion;document.getElementById('certificate-print').onclick=()=>window.print();
  }

  function renderBadgeDesigner(){
    mapView.innerHTML=`<section class="badge-designer"><button id="designer-back" class="primary-button">← Celebration</button><p class="champion-kicker">SECRET BONUS UNLOCKED!</p><h1>Design Your Own Faith-Trails Badge</h1><p>Choose your badge color, symbol, and special name. Then download your creation!</p><div class="designer-grid"><div class="designer-controls"><label>Badge name<input id="custom-badge-name" maxlength="24" value="Faithful Explorer"></label><fieldset><legend>Choose a color</legend><div id="badge-colors" class="design-options"></div></fieldset><fieldset><legend>Choose a symbol</legend><div id="badge-symbols" class="design-options"></div></fieldset><button id="download-custom-badge" class="primary-button">⬇️ Download My Badge</button></div><div class="designer-preview"><canvas id="custom-badge-canvas" width="800" height="800"></canvas></div></div></section>`;
    document.getElementById('designer-back').onclick=renderChampion;
    const colors=['#D9A73B','#2F8F50','#3B7A9C','#7B5CA8','#D85A30','#E66FA5'],symbols=['🧭','🏆','🌟','🦁','🪨','🐋','🌈','🙏'];let color=colors[0],symbol=symbols[0];const canvas=document.getElementById('custom-badge-canvas'),ctx=canvas.getContext('2d'),name=document.getElementById('custom-badge-name');
    const select=(button,box)=>{box.querySelectorAll('.selected').forEach(x=>x.classList.remove('selected'));button.classList.add('selected')};
    colors.forEach((x,i)=>{const b=button('',()=>{color=x;select(b,document.getElementById('badge-colors'));drawBadge()},'design-choice design-color'+(i?'':' selected'));b.style.background=x;document.getElementById('badge-colors').appendChild(b)});symbols.forEach((x,i)=>{const b=button(x,()=>{symbol=x;select(b,document.getElementById('badge-symbols'));drawBadge()},'design-choice design-symbol'+(i?'':' selected'));document.getElementById('badge-symbols').appendChild(b)});
    function drawBadge(){ctx.clearRect(0,0,800,800);const g=ctx.createRadialGradient(330,250,20,400,400,370);g.addColorStop(0,'#fff8c9');g.addColorStop(.45,color);g.addColorStop(1,'#6b4700');ctx.fillStyle=g;ctx.beginPath();ctx.arc(400,400,360,0,Math.PI*2);ctx.fill();ctx.lineWidth=28;ctx.strokeStyle='#fff3b0';ctx.stroke();ctx.lineWidth=10;ctx.strokeStyle='#5c3b00';ctx.stroke();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font='210px serif';ctx.fillText(symbol,400,330);ctx.fillStyle='#fff';ctx.strokeStyle='#3A2E20';ctx.lineWidth=10;let size=74,label=(name.value.trim()||'Faithful Explorer').toUpperCase();do{ctx.font=`800 ${size}px Nunito`;size-=2}while(ctx.measureText(label).width>620&&size>30);ctx.strokeText(label,400,560);ctx.fillText(label,400,560);ctx.font='700 35px Nunito';ctx.fillStyle='#fff8d6';ctx.fillText('FAITH-TRAILS CHAMPION',400,650)}
    name.oninput=drawBadge;drawBadge();document.getElementById('download-custom-badge').onclick=()=>{const a=document.createElement('a');a.download='my-faith-trails-badge.png';a.href=canvas.toDataURL('image/png');a.click()};
  }

  function championConfetti(){const c=document.getElementById('grand-confetti');if(!c)return;const x=c.getContext('2d'),host=c.parentElement;c.width=host.clientWidth;c.height=host.clientHeight;const colors=['#ffd76a','#f5b82e','#fff3b0','#2f8f50','#6bb8d8'],pieces=Array.from({length:110},()=>({x:Math.random()*c.width,y:-Math.random()*c.height,s:4+Math.random()*7,v:1.5+Math.random()*3,d:(Math.random()-.5)*1.5,c:colors[Math.floor(Math.random()*colors.length)]}));let frames=0;(function draw(){x.clearRect(0,0,c.width,c.height);pieces.forEach(p=>{p.y+=p.v;p.x+=p.d;if(p.y>c.height){p.y=-10;p.x=Math.random()*c.width}x.fillStyle=p.c;x.fillRect(p.x,p.y,p.s,p.s*.55)});if(frames++<900)requestAnimationFrame(draw)})()}
  function confetti(){const c=document.getElementById('confetti-canvas'),x=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;let p=Array.from({length:100},()=>({x:Math.random()*c.width,y:-Math.random()*c.height,s:4+Math.random()*8,v:2+Math.random()*4,d:Math.random()*2-1,h:Math.random()*360})),n=0;function go(){x.clearRect(0,0,c.width,c.height);p.forEach(q=>{q.y+=q.v;q.x+=q.d;x.fillStyle=`hsl(${q.h} 80% 55%)`;x.fillRect(q.x,q.y,q.s,q.s*.6)});if(n++<420&&document.getElementById('badge-overlay').classList.contains('open'))requestAnimationFrame(go)}go()}
  document.querySelectorAll('[data-game-home]').forEach(b=>b.onclick=e=>{e.preventDefault();if(!questView.hidden)showMap();else renderMap()});window.onpopstate=e=>{if(e.state?.view==='quest')openQuest(e.state.slug,false);else if(!questView.hidden)transition(questView,mapView,renderMap)};
  document.querySelectorAll('[data-game-screen]').forEach(a=>a.onclick=e=>{e.preventDefault();if(!questView.hidden){transition(questView,mapView,()=>renderCollection(a.dataset.gameScreen))}else renderCollection(a.dataset.gameScreen)});
  // Debounce resize events so the SVG trail is recalculated once after the
  // viewport settles instead of on every pixel of a resize gesture.
  let trailResizeTimer;window.addEventListener('resize',()=>{clearTimeout(trailResizeTimer);trailResizeTimer=setTimeout(drawFaithTrail,120)});
  renderMap();if(boot.initialQuest)openQuest(boot.initialQuest,false);
})();
