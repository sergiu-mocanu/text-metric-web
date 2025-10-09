function selectAllMetrics(){
    const selectAll = document.getElementById('select_all');
    const checkboxes = document.querySelectorAll('.metric_checkbox');
    selectAll.addEventListener('change', function() {
        checkboxes.forEach(cb => cb.checked = this.checked);
    });
}


function iniLoadingOverlay() {
    const form = document.querySelector('form');
    const loading = document.getElementById('loading-overlay');
    form.addEventListener('submit', () => {
        loading.style.display = 'block';
    });
}


function manageLoadingOverlay() {
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
}


function collapseExpandScripts() {
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
}


function resultsVisualization() {
    const chartCanvas = document.getElementById('metricsChart');
    const chartDataEl = document.getElementById('chartData');

    const metricColors = {
        "BLEU": "rgba(0, 123, 255, 0.6)",
        "CodeBLEU": "rgba(220, 53, 69, 0.6)",
        "ROUGE": "rgba(40, 167, 69, 0.6)",
        "METEOR": "rgba(255, 193, 7, 0.6)",
        "ChrF": "rgba(150, 7, 220, 0.6)"
    };

    if (chartCanvas && chartDataEl) {
        const data = JSON.parse(chartDataEl.textContent);

        if (data['CodeBLEU']) { data['CodeBLEU'] = data['CodeBLEU']['codebleu']; }

        const labels = Object.keys(data)
        const scoreValues = Object.values(data)

        const backgroundColors = labels.map(m => metricColors[m] || "rgba(108,117,125,0.6)")
        new Chart(chartCanvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Similarity Scores',
                    data: scoreValues,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 1,
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, max: 1}
                },
                plugins: {
                    legend: { display: false}
                },
                barThickness: 'flex',
                maxBarThickness: 100,
            }
        })
    }
}


selectAllMetrics();

iniLoadingOverlay();
manageLoadingOverlay();

collapseExpandScripts();

resultsVisualization();
