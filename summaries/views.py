# summaries/views.py

import google.generativeai as genai
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadAudioForm
from .models import Summary

# Configure the Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)

def upload_view(request):
    if request.method == 'POST':
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            summary_obj = form.save()
            try:
                audio_file_path = summary_obj.audio_file.path
                uploaded_file = genai.upload_file(path=audio_file_path)

                prompt = (
                    "Please transcribe the following audio file. After transcribing, "
                    "provide a concise summary of the meeting and a list of clear, "
                    "actionable items. Structure your response with the following headers: "
                    "'Transcript:', 'Summary:', and 'Action Items:'"
                )

                model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
                response = model.generate_content([prompt, uploaded_file])

                full_text = response.text
                
                transcript_part = full_text.split("Summary:")[0].replace("Transcript:", "").strip()
                summary_part = full_text.split("Action Items:")[0].split("Summary:")[1].strip()
                action_items_part = full_text.split("Action Items:")[1].strip()

                summary_obj.transcript = transcript_part
                summary_obj.summary = summary_part
                summary_obj.action_items = action_items_part
                summary_obj.save()

                return redirect('summary_detail', pk=summary_obj.pk)
            
            except Exception as e:
                summary_obj.summary = f"An error occurred: {e}"
                summary_obj.save()
                return redirect('summary_detail', pk=summary_obj.pk)
    else:
        form = UploadAudioForm()
    
    return render(request, 'summaries/upload.html', {'form': form})

def summary_detail_view(request, pk):
    summary = get_object_or_404(Summary, pk=pk)
    return render(request, 'summaries/detail.html', {'summary': summary})