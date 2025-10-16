# summaries/forms.py

from django import forms
from .models import Summary

class UploadAudioForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['audio_file']
        labels = {
            'audio_file': 'Upload your meeting audio file'
        }