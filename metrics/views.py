from django.shortcuts import render

from .analysis import calculate_metric, TextMetric, metric_to_title
import time

def metrics_view(request):
    similarity_scores = {}
    available_metrics = [m.value for m in TextMetric]
    error_message = None
    selected_metrics = []

    if request.method == 'POST':
        reference = request.POST.get('baseline', '')
        prediction = request.POST.get('prediction', '')
        selected_metrics = request.POST.getlist('metrics', '')

        if not reference or not prediction:
            error_message = 'Both scripts must be provided.'
        elif not selected_metrics:
            error_message = 'Select at least one metric.'
        else:
            for metric_name in selected_metrics:
                metric = TextMetric(metric_name)
                metric_title = metric_to_title(metric)
                similarity_scores[metric_title] = calculate_metric(metric=metric, baseline_script=reference,
                                                    ai_script=prediction)

    return render(request, 'metrics/form.html', {
        'similarity_scores': similarity_scores,
        'available_metrics': available_metrics,
        'error_message': error_message,
        'selected_metrics': selected_metrics
    })
