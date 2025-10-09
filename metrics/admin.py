from django.contrib import admin
from .models import Comparison, Metric

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_metrics_used', 'results', 'created_at')
    search_fields = ('get_metrcs_used',)
    ordering = ('created_at',)

    def get_metrics_used(self, obj):
        return ', '.join(m.name for m in obj.metrics_used.all())
    get_metrics_used.short_description = 'Metrics used'


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
