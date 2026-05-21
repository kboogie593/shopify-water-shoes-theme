// AquaStep Theme JS

document.addEventListener('DOMContentLoaded', () => {
  initMenuToggle();
  initQuantityInputs();
  initProductGallery();
  initVariantSelectors();
  initCartDrawer();
  initSearchDrawer();
  initCookieBanner();
  initProductFormAjax();
});

/* ---------- Menu ---------- */
function initMenuToggle() {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.header-nav');
  if (!toggle || !nav) return;
  toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
}

/* ---------- Quantity steppers ---------- */
function initQuantityInputs() {
  document.querySelectorAll('.product-quantity').forEach((wrapper) => {
    if (wrapper.dataset.qtyInit) return;
    wrapper.dataset.qtyInit = '1';
    const input = wrapper.querySelector('input[type="number"]');
    const minus = wrapper.querySelector('[data-action="minus"]');
    const plus = wrapper.querySelector('[data-action="plus"]');
    if (!input) return;
    minus?.addEventListener('click', () => {
      const v = Math.max(0, (parseInt(input.value, 10) || 1) - 1);
      input.value = v;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
    plus?.addEventListener('click', () => {
      const v = (parseInt(input.value, 10) || 1) + 1;
      input.value = v;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });
}

/* ---------- Product gallery ---------- */
function initProductGallery() {
  const gallery = document.querySelector('[data-product-gallery]');
  if (!gallery) return;
  const main = gallery.querySelector('[data-gallery-main] img');
  const thumbs = gallery.querySelectorAll('[data-gallery-thumb]');
  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', () => {
      const src = thumb.dataset.src;
      const alt = thumb.dataset.alt || '';
      if (main && src) { main.src = src; main.alt = alt; }
      thumbs.forEach((t) => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });
}

/* ---------- Variant selectors ---------- */
function initVariantSelectors() {
  const form = document.querySelector('[data-product-form]');
  if (!form) return;
  const variantInput = form.querySelector('input[name="id"]');
  const priceEl = document.querySelector('[data-product-price]');
  const submitBtn = form.querySelector('[data-add-to-cart]');
  const variantsTag = document.querySelector('[data-product-variants]');
  if (!variantsTag) return;
  let variants = [];
  try { variants = JSON.parse(variantsTag.textContent); } catch (e) { return; }

  form.querySelectorAll('input[data-option-name]').forEach((input) => {
    input.addEventListener('change', () => {
      const chosen = collectChosen(form);
      const match = variants.find((v) =>
        chosen.every((c, idx) => v.options[idx] === c),
      );
      if (match) {
        if (variantInput) variantInput.value = match.id;
        if (priceEl && match.price != null) priceEl.textContent = formatMoney(match.price);
        if (submitBtn) {
          submitBtn.disabled = !match.available;
          submitBtn.textContent = match.available ? 'Add to cart' : 'Sold out';
        }
      }
    });
  });
}

function collectChosen(form) {
  const groups = {};
  form.querySelectorAll('input[type="radio"][data-option-name]').forEach((r) => {
    if (r.checked) groups[r.dataset.optionName] = r.value;
  });
  return Object.values(groups);
}

function formatMoney(cents) {
  const dollars = (cents / 100).toFixed(2);
  return `$${dollars}`;
}

/* ---------- Cart Drawer ---------- */
function initCartDrawer() {
  const drawer = document.querySelector('[data-cart-drawer]');
  if (!drawer) return;

  const openTriggers = document.querySelectorAll('[data-cart-open]');
  const closeTriggers = drawer.querySelectorAll('[data-cart-close]');

  const open = () => {
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };
  const close = () => {
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  openTriggers.forEach((t) => t.addEventListener('click', (e) => { e.preventDefault(); open(); }));
  closeTriggers.forEach((t) => t.addEventListener('click', close));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });

  // Delegate quantity & remove inside drawer
  drawer.addEventListener('click', async (e) => {
    const change = e.target.closest('[data-cart-qty-change]');
    const remove = e.target.closest('[data-cart-remove]');
    if (change) {
      const delta = parseInt(change.dataset.cartQtyChange, 10);
      const line = parseInt(change.dataset.line, 10);
      const input = drawer.querySelector(`[data-cart-qty][data-line="${line}"]`);
      const next = Math.max(0, (parseInt(input.value, 10) || 0) + delta);
      input.value = next;
      await updateCartLine(line, next);
    }
    if (remove) {
      const line = parseInt(remove.dataset.line, 10);
      await updateCartLine(line, 0);
    }
  });
  drawer.addEventListener('change', async (e) => {
    const qty = e.target.closest('[data-cart-qty]');
    if (qty) {
      const line = parseInt(qty.dataset.line, 10);
      const next = Math.max(0, parseInt(qty.value, 10) || 0);
      await updateCartLine(line, next);
    }
  });

  // Expose openCart globally
  window.aquaCart = { open, close, refresh: refreshCart };
}

async function updateCartLine(line, quantity) {
  try {
    await fetch('/cart/change.js', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ line, quantity }),
    });
    await refreshCart();
  } catch (err) {
    console.error('cart change failed', err);
  }
}

async function refreshCart() {
  try {
    const res = await fetch(window.location.pathname + '?sections=cart-drawer-section', { headers: { Accept: 'application/json' } });
    if (res.ok) {
      // Re-render via section render API would require a section. Fallback: full re-fetch.
    }
    // Simpler: re-fetch the current page and swap the drawer markup.
    const html = await fetch(window.location.pathname, { headers: { Accept: 'text/html' } }).then((r) => r.text());
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const newDrawer = doc.querySelector('[data-cart-drawer]');
    const oldDrawer = document.querySelector('[data-cart-drawer]');
    if (newDrawer && oldDrawer) {
      const wasOpen = oldDrawer.getAttribute('aria-hidden') === 'false';
      oldDrawer.innerHTML = newDrawer.innerHTML;
      if (wasOpen) oldDrawer.setAttribute('aria-hidden', 'false');
    }
    const newBubble = doc.querySelector('[data-cart-count-bubble]');
    const oldBubble = document.querySelector('[data-cart-count-bubble]');
    if (newBubble && oldBubble) {
      oldBubble.textContent = newBubble.textContent;
      const count = parseInt(newBubble.textContent, 10);
      if (count > 0) oldBubble.removeAttribute('hidden');
      else oldBubble.setAttribute('hidden', '');
    }
  } catch (err) {
    console.error('cart refresh failed', err);
  }
}

/* ---------- Product form AJAX (so add-to-cart opens drawer) ---------- */
function initProductFormAjax() {
  const form = document.querySelector('[data-product-form]');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    if (!window.aquaCart) return; // fall back to default
    e.preventDefault();
    const submitBtn = form.querySelector('[data-add-to-cart]');
    const originalText = submitBtn?.textContent;
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Adding...'; }
    try {
      const formData = new FormData(form);
      const res = await fetch('/cart/add.js', {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: formData,
      });
      if (!res.ok) throw new Error('add failed');
      await refreshCart();
      window.aquaCart.open();
    } catch (err) {
      console.error(err);
      form.submit();
    } finally {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalText; }
    }
  });
}

/* ---------- Search Drawer + Predictive ---------- */
function initSearchDrawer() {
  const drawer = document.querySelector('[data-search-drawer]');
  if (!drawer) return;
  const input = drawer.querySelector('[data-search-input]');
  const results = drawer.querySelector('[data-search-results]');
  const openTriggers = document.querySelectorAll('[data-search-open]');
  const closeTriggers = drawer.querySelectorAll('[data-search-close]');

  const open = () => {
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setTimeout(() => input?.focus(), 250);
  };
  const close = () => {
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };
  openTriggers.forEach((t) => t.addEventListener('click', (e) => { e.preventDefault(); open(); }));
  closeTriggers.forEach((t) => t.addEventListener('click', close));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
    if (e.key === '/' && e.target === document.body) { e.preventDefault(); open(); }
  });

  let timer;
  const initialHTML = results.innerHTML;
  input?.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 2) {
      results.innerHTML = initialHTML;
      return;
    }
    results.innerHTML = '<div class="search-drawer__loading">Searching…</div>';
    timer = setTimeout(() => predictiveSearch(q, results), 220);
  });
}

async function predictiveSearch(query, container) {
  try {
    const url = `/search/suggest.json?q=${encodeURIComponent(query)}&resources[type]=product,collection,article&resources[limit]=6`;
    const data = await fetch(url, { headers: { Accept: 'application/json' } }).then((r) => r.json());
    const products = data?.resources?.results?.products || [];
    const collections = data?.resources?.results?.collections || [];

    if (products.length === 0 && collections.length === 0) {
      container.innerHTML = '<div class="search-drawer__loading">No matches. Try another search.</div>';
      return;
    }

    let html = '';
    if (collections.length > 0) {
      html += '<div style="margin-bottom:20px"><span class="eyebrow" style="display:block;margin-bottom:10px;background:none;padding:0">Collections</span><div class="search-drawer__suggestions">';
      collections.forEach((c) => {
        html += `<a href="${c.url}">${escapeHtml(c.title)}</a>`;
      });
      html += '</div></div>';
    }
    if (products.length > 0) {
      html += '<span class="eyebrow" style="display:block;margin-bottom:10px;background:none;padding:0">Products</span>';
      html += '<div class="search-drawer__product-results">';
      products.forEach((p) => {
        const img = p.image || p.featured_image?.url || '';
        const price = formatMoney(parseFloat(p.price || 0) * 100);
        html += `
          <a class="search-drawer__product" href="${p.url}">
            <div class="search-drawer__product-image">${img ? `<img src="${img}" alt="${escapeHtml(p.title)}" loading="lazy">` : ''}</div>
            <div class="search-drawer__product-title">${escapeHtml(p.title)}</div>
            <div class="search-drawer__product-price">${price}</div>
          </a>`;
      });
      html += '</div>';
    }
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = '<div class="search-drawer__loading">Search unavailable. Please try again.</div>';
  }
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
}

/* ---------- Cookie Banner ---------- */
function initCookieBanner() {
  const banner = document.querySelector('[data-cookie-banner]');
  if (!banner) return;
  const stored = localStorage.getItem('aqua_cookie_consent');
  if (stored) return;
  banner.hidden = false;
  banner.addEventListener('click', (e) => {
    const action = e.target.closest('[data-cookie-action]');
    if (!action) return;
    localStorage.setItem('aqua_cookie_consent', action.dataset.cookieAction);
    banner.hidden = true;
  });
}
