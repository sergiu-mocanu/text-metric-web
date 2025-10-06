from django.shortcuts import render

from .analysis import calculate_metric, TextMetric, metric_to_title

def metrics_view(request):
    similarity_scores = {}
    available_metrics = [m.value for m in TextMetric]
    error_message = None
    baseline_script = ''
    ai_script = ''
    selected_metrics = []

    if request.method == 'POST':
        baseline_script = request.POST.get('baseline_script', '')
        ai_script = request.POST.get('ai_script', '')
        selected_metrics = request.POST.getlist('metrics', '')

        if not baseline_script or not ai_script:
            error_message = 'Both scripts must be provided.'
        elif not selected_metrics:
            error_message = 'Select at least one metric.'
        else:
            for metric_name in selected_metrics:
                metric = TextMetric(metric_name)
                metric_title = metric_to_title(metric)
                similarity_scores[metric_title] = calculate_metric(metric=metric, baseline_script=baseline_script,
                                                    ai_script=ai_script)

    return render(request, 'metrics/form.html', {
        'similarity_scores': similarity_scores,
        'available_metrics': available_metrics,
        'error_message': error_message,
        'baseline_script': baseline_script,
        'ai_script': ai_script,
        'selected_metrics': selected_metrics
    })
