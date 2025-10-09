from django.db import models


class Metric(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Comparison(models.Model):
    baseline_script = models.TextField()
    ai_script = models.TextField()
    metrics_used = models.ManyToManyField(Metric)
    results = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comparison {self.id} ({self.created_at:%Y-%m-%d %H:%M}'

