# summaries/models.py

from django.db import models

class Summary(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    action_items = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.audio_file.name}"