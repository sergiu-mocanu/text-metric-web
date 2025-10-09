from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

class MetricsViewTests(TestCase):
    def test_index_page_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Textual Similarity Metrics')