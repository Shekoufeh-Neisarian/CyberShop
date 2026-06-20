// ── Cart count ───────────────────────────────────────────────────────────────

function updateCartCount(count) {
  const el = document.getElementById('cart-count');
  if (!el) return;
  el.textContent = count;
  el.classList.add('bump');
  setTimeout(() => el.classList.remove('bump'), 200);
}

fetch('/api/cart')
  .then(r => r.json())
  .then(data => updateCartCount(data.count))
  .catch(() => {});


// ── Sidebar ──────────────────────────────────────────────────────────────────

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const reopenBtn = document.getElementById('sidebarReopenBtn');
  if (!sidebar) return;
  const collapsed = sidebar.classList.toggle('collapsed');
  reopenBtn && reopenBtn.classList.toggle('hidden', !collapsed);
  localStorage.setItem('sidebarCollapsed', collapsed ? '1' : '0');
}

function toggleTopic(id) {
  const topic = document.getElementById('st-' + id);
  if (!topic) return;
  const body = topic.querySelector('.sidebar-topic-body');
  const chevron = topic.querySelector('.sidebar-chevron');
  const isOpen = body.classList.toggle('open');
  if (chevron) chevron.style.transform = isOpen ? 'rotate(180deg)' : '';
}

// Restore sidebar state and auto-scroll active topic into view
(function() {
  const sidebar = document.getElementById('sidebar');
  const reopenBtn = document.getElementById('sidebarReopenBtn');
  if (!sidebar) return;
  if (localStorage.getItem('sidebarCollapsed') === '1') {
    sidebar.classList.add('collapsed');
    reopenBtn && reopenBtn.classList.remove('hidden');
  }
  // scroll sidebar so active topic btn is visible (not the body, just the btn)
})();


// ── Inspector ────────────────────────────────────────────────────────────────

function toggleInspector() {
  const drawer = document.getElementById('inspectorDrawer');
  if (!drawer) return;
  drawer.classList.toggle('open');
  if (drawer.classList.contains('open')) loadSessionData();
}

function loadSessionData() {
  const el = document.getElementById('sessionData');
  if (!el) return;
  fetch('/api/cart')
    .then(r => r.json())
    .then(data => {
      const info = {
        cart: data.items.reduce((acc, item) => { acc[item.id] = item.quantity; return acc; }, {}),
        cart_count: data.count,
        logged_in: !!document.querySelector('a[href*="logout"]'),
      };
      el.textContent = JSON.stringify(info, null, 2);
    })
    .catch(() => { el.textContent = 'unavailable'; });
}

// Body padding for fixed inspector bar
(function() {
  const bar = document.getElementById('inspectorBar');
  if (bar) {
    document.querySelector('footer') && (document.querySelector('footer').style.marginBottom = bar.offsetHeight + 'px');
  }
})();


// ── AI chat widget ────────────────────────────────────────────────────────────

function toggleAI() {
  const panel = document.getElementById('aiChatPanel');
  if (!panel) return;
  panel.classList.toggle('open');
}

function askAI() {
  const input = document.getElementById('aiQuestion');
  const q = input ? input.value.trim() : '';
  if (!q) return;

  const resp = document.getElementById('aiResponse');
  const badge = document.getElementById('aiBadge');
  const btn = document.getElementById('aiBtn');

  if (resp) { resp.className = 'ai-response loading'; resp.textContent = '…'; }
  if (badge) badge.classList.add('hidden');
  if (btn) btn.disabled = true;

  fetch('/api/ai/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: q })
  })
  .then(r => r.json())
  .then(data => {
    if (resp) { resp.className = 'ai-response'; resp.textContent = data.answer; }
    if (badge) {
      badge.classList.remove('hidden');
      if (data.live) { badge.className = 'ai-live-badge'; badge.textContent = '✓ Live Gemini response'; }
      else { badge.className = 'ai-offline-badge'; badge.textContent = data.answer.includes('Offline') ? '' : '(offline mode)'; }
    }
    if (btn) btn.disabled = false;
  })
  .catch(() => {
    if (resp) { resp.className = 'ai-response error'; resp.textContent = 'Something went wrong.'; }
    if (btn) btn.disabled = false;
  });
}
