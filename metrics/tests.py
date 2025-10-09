from django.test import TestCase
from django.urls import reverse

from metrics.analysis import TextMetric, calculate_metric
from metrics.models import Metric, Comparison


class PageTests(TestCase):
    def test_main_page_loads(self):
        response = self.client.get(reverse('metrics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Textual Similarity Metrics')


class MetricsPostTests(TestCase):
    def test_missing_scripts_returns_error(self):
        response = self.client.post(reverse('metrics'), {
            'baseline_script': [],
            'ai_script': [],
            'metrics': [TextMetric.BL.alias]
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Both scripts must be provided.')

    def test_missing_metrics_returns_error(self):
        response = self.client.post(reverse('metrics'), {
            'baseline_script': 'print("Hi")',
            'ai_script': 'print("Hello")',
            'metrics': []
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select at least one metric.')


class MetricComputationTests(TestCase):
    def test_bleu_returns_float(self):
        score = calculate_metric(TextMetric.BL, 'print("Hello")', 'print("Hi")')
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_codebleu_returns_dict(self):
        score = calculate_metric(TextMetric.CB, 'print("Hello")', 'print("Hi")')
        self.assertIsInstance(score, dict)
        self.assertIn('codebleu', score)


class DatabaseTests(TestCase):
    def setUp(self):
        self.metric = Metric.objects.create(name=TextMetric.RG.alias)

    def test_post_creates_comparison_entry(self):
        self.assertEqual(Comparison.objects.count(), 0)
        self.client.post(reverse('metrics'), {
            'baseline_script': 'print("Hello")',
            'ai_script': 'print("Hi")',
            'metrics': [TextMetric.BL.alias]
        })
        self.assertEqual(Comparison.objects.count(), 1)

    def test_create_comparison(self):
        comparison = Comparison.objects.create(
            baseline_script='print("Hello")',
            ai_script='print("Hi")',
            results={TextMetric.RG.alias: 0.5}
        )
        comparison.metrics_used.add(self.metric)
        self.assertEqual(comparison.metrics_used.count(), 1)


class FilteringTests(TestCase):
    def setUp(self):
        baseline = 'print("Hello")'
        ai = 'print("Hi")'
        bleu_alias = TextMetric.BL.alias
        rouge_alias = TextMetric.RG.alias
        self.metric_bleu = Metric.objects.create(name=bleu_alias)
        self.metric_rouge = Metric.objects.create(name=rouge_alias)
        c1 = Comparison.objects.create(baseline_script=baseline, ai_script=ai, results={bleu_alias: 0.0})
        c1.metrics_used.add(self.metric_bleu)
        c2 = Comparison.objects.create(baseline_script=baseline, ai_script=ai, results={rouge_alias: 0.5})
        c2.metrics_used.add(self.metric_rouge)

    def test_filtering_by_metric(self):
        results = Comparison.objects.filter(metrics_used__name=TextMetric.BL.alias)
        self.assertEqual(results.count(), 1)


class ChartContextTests(TestCase):
    def test_chart_data_and_results_in_context(self):
        response = self.client.post(reverse('metrics'), {
            'baseline_script': 'print("Hello")',
            'ai_script': 'print("Hi")',
            'metrics': [TextMetric.BL.alias]
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('similarity_scores', response.context)
        self.assertIn('chart_data', response.context)

        scores = response.context['similarity_scores']
        chart_data = response.context['chart_data']

        self.assertIsInstance(scores, dict)
        self.assertTrue(chart_data)
