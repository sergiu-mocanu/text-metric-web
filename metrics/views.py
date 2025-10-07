from django.shortcuts import render
from .models import Comparison

from .analysis import calculate_metric, TextMetric, round_results


def metrics_view(request):
    similarity_scores = {}
    available_metrics = [m.alias for m in TextMetric]
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
            for metric_title in selected_metrics:
                metric = TextMetric.from_alias(metric_title)
                similarity_score = calculate_metric(metric=metric, baseline_script=baseline_script,
                                                    ai_script=ai_script)
                rounded = round_results(similarity_score)
                similarity_scores[metric_title] = rounded

            Comparison.objects.create(
                baseline_script=baseline_script,
                ai_script=ai_script,
                metrics_used=', '.join(selected_metrics),
                results=similarity_scores
            )

    recent = Comparison.objects.order_by('-created_at')[:5]

    return render(request, 'metrics/form.html', {
        'similarity_scores': similarity_scores,
        'available_metrics': available_metrics,
        'error_message': error_message,
        'baseline_script': baseline_script,
        'ai_script': ai_script,
        'selected_metrics': selected_metrics,
        'recent': recent,
    })
