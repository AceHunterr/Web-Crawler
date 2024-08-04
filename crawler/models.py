from django.db import models

class WebPage(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    visits = models.IntegerField(default=0)
    crawled_at = models.DateTimeField(auto_now_add=True)
    report = models.JSONField(default=dict)  # Add this field to store the crawl report as JSON
