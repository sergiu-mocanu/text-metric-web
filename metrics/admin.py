from django.contrib import admin
from .models import Comparison

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('id', 'metrics_used', 'results', 'created_at')
    search_fields = ('metrics_used',)
    ordering = ('created_at',)
