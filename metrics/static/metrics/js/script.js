const selectAll = document.getElementById('select_all');
const checkboxes = document.querySelectorAll('.metric_checkbox');
selectAll.addEventListener('change', function() {
    checkboxes.forEach(cb => cb.checked = this.checked);
});

const form = document.querySelector('form');
const loading = document.getElementById('loading-overlay');
form.addEventListener('submit', () => {
    loading.style.display = 'block';
});

document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('loading-overlay');
    const form = document.querySelector('form');

    if (overlay) overlay.setAttribute('aria-hidden', 'true');

    if (!form || !overlay) {
        return;
    }

    form.addEventListener('submit', function(e) {
        const valid = typeof form.checkValidity === 'function' ? form.checkValidity() : true;
        if (valid) {
            overlay.setAttribute('aria-hidden', 'false');
        } else {
            if (typeof form.reportValidity === 'function') form.reportValidity();
        }
    });
    window.addEventListener('pageshow', () => overlay.setAttribute('aria-hidden', 'true'));
});

document.querySelectorAll('.toggle-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const li = this.parentElement;
        const excerpt = li.querySelector('.excerpt');
        const full = li.querySelector('.full-text');

        if (full.style.display === 'none') {
            full.style.display = 'block';
            excerpt.style.display = 'none';
            this.textContent = 'Show less';
        } else {
            full.style.display = 'none';
            excerpt.style.display = 'block';
            this.textContent = 'Show more';
        }
    });
});