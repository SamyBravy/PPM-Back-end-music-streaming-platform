// Use a flag to avoid adding multiple event listeners when HTMX re-evaluates scripts
if (!window.themeToggleInitialized) {
    window.themeToggleInitialized = true;

    window.updateIcon = function () {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const btns = document.querySelectorAll('.theme-toggle');
        btns.forEach(btn => {
            btn.innerHTML = currentTheme === 'dark' ? '☀️' : '🌙';
        });
    };

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.theme-toggle');
        if (btn) {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            window.updateIcon();
        }
    });

    document.body.addEventListener('htmx:load', function (evt) {
        if (window.updateIcon) window.updateIcon();
    });

    document.body.addEventListener('htmx:afterRequest', function () {
        const navbarCollapse = document.getElementById('navbarNav');
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            const bsCollapse = new bootstrap.Collapse(navbarCollapse, { toggle: false });
            bsCollapse.hide();
        }
    });
}

// Execute on every load
if (window.updateIcon) window.updateIcon();

// Global Player Logic
function playGlobalSong(url, title, artist, detailUrl) {
    const container = document.getElementById('global-player-container');
    const audio = document.getElementById('global-audio');
    if (!container || !audio) return;

    const titleEl = document.getElementById('gp-title');
    if (detailUrl) {
        titleEl.innerHTML = `<a href="${detailUrl}" class="text-decoration-none" style="color: inherit;">${title}</a>`;
    } else {
        titleEl.innerText = title;
    }

    document.getElementById('gp-artist').innerText = artist;

    audio.src = url;
    container.style.display = 'block';
    audio.play().catch(e => console.log('Autoplay prevented', e));
}

function closeGlobalPlayer() {
    const container = document.getElementById('global-player-container');
    const audio = document.getElementById('global-audio');
    if (audio) {
        audio.pause();
        audio.src = '';
    }
    if (container) container.style.display = 'none';
}
