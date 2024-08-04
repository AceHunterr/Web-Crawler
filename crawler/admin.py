from django.contrib import admin
from .models import WebPage

@admin.register(WebPage)
class WebPageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'visits', 'crawled_at')
    search_fields = ('url', 'title')
    readonly_fields = ('crawled_at',)

# Alternatively, you can use admin.site.register without the decorator:
# admin.site.register(WebPage, WebPageAdmin)
