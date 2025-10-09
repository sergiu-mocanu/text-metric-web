from django.shortcuts import render
from .models import Comparison

import json

from .analysis import calculate_metric, TextMetric, round_results


def metrics_view(request):
    similarity_scores: dict[str, float] = {}
    error_message: str | None = None
    baseline_script: str = ''
    ai_script: str = ''
    available_metrics: list[str] = [m.alias for m in TextMetric]
    selected_metrics: list[str] = []
    comparison: Comparison | None = None

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

            comparison = Comparison.objects.create(
                baseline_script=baseline_script,
                ai_script=ai_script,
                metrics_used=', '.join(selected_metrics),
                results=similarity_scores
            )

    previous_results = Comparison.objects.all().order_by('-created_at')
    if comparison is not None:
        previous_results = previous_results.exclude(id=comparison.id)

    selected_filter = request.GET.get('filter_metric')
    if selected_filter and selected_filter != 'All':
        previous_results = previous_results.filter(metrics_used__contains=selected_filter)

    previous_results = previous_results[:5]

    return render(request, 'metrics/form.html', {
        'similarity_scores': similarity_scores,
        'chart_data': json.dumps(similarity_scores),
        'available_metrics': available_metrics,
        'selected_metrics': selected_metrics,
        'baseline_script': baseline_script,
        'ai_script': ai_script,
        'error_message': error_message,
        'previous_results': previous_results,
        'selected_filter': selected_filter,
    })
