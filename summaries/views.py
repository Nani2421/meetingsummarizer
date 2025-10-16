# summaries/views.py

import google.generativeai as genai
import logging
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadAudioForm
from .models import Summary
import re

# Configure the Gemini API
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Set up logging
logger = logging.getLogger(__name__)

def upload_view(request):
    if request.method == 'POST':
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            summary_obj = form.save()
            try:
                audio_file_path = summary_obj.audio_file.path

                # Ensure the file is uploaded with a display name
                uploaded_file = genai.files.upload_file(
                    path=audio_file_path,
                    display_name=summary_obj.audio_file.name
                )

                prompt = (
                    "Please transcribe the following audio file. After transcribing, "
                    "provide a concise summary of the meeting and a list of clear, "
                    "actionable items. Structure your response with the following headers: "
                    "'Transcript:', 'Summary:', and 'Action Items:'. If the audio is unclear, "
                    "indicate that the transcript could not be generated."
                )

                model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
                response = model.generate_content([prompt, uploaded_file])

                full_text = response.text
                
                # Use regex to robustly parse the response
                transcript_match = re.search(r"Transcript:(.*?)Summary:", full_text, re.DOTALL)
                summary_match = re.search(r"Summary:(.*?)Action Items:", full_text, re.DOTALL)
                action_items_match = re.search(r"Action Items:(.*)", full_text, re.DOTALL)

                summary_obj.transcript = transcript_match.group(1).strip() if transcript_match else "Transcript not available."
                summary_obj.summary = summary_match.group(1).strip() if summary_match else "Summary not available."
                summary_obj.action_items = action_items_match.group(1).strip() if action_items_match else "No action items identified."

                summary_obj.save()

                return redirect('summary_detail', pk=summary_obj.pk)
            
            except Exception as e:
                # Log the full exception for debugging
                logger.error("An error occurred during Gemini API call", exc_info=True)
                summary_obj.summary = f"An error occurred: {e}. Check logs for details."
                summary_obj.save()
                return redirect('summary_detail', pk=summary_obj.pk)
    else:
        form = UploadAudioForm()
    
    return render(request, 'summaries/upload.html', {'form': form})

def summary_detail_view(request, pk):
    summary = get_object_or_404(Summary, pk=pk)
    return render(request, 'summaries/detail.html', {'summary': summary})