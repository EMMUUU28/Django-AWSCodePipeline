# RoadMMap
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
from django.shortcuts import render
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))

def roadmap1(request):
    url = 'https://roadmap.sh/pdfs/roadmaps/python.pdf'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Set the appropriate content type for PDF files
        file_response = FileResponse(response.content, content_type='application/pdf')
        file_response['Content-Disposition'] = 'attachment; filename="python.pdf"'
        return file_response
    else:
        return HttpResponse("Failed to download PDF", status=response.status_code)



def roadmap(request):
    
    if request.method == 'POST':
        selected_roadmap = request.POST.get('roadmap', 'python')
        # Use selected_roadmap as needed
        url = f'https://roadmap.sh/pdfs/roadmaps/{selected_roadmap}.pdf'
    else:
        selected_roadmap='python'
        url = f'https://roadmap.sh/pdfs/roadmaps/{selected_roadmap}.pdf'
    
    if request.method == 'POST':

        user_input = request.POST.get('user_question')   
        genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
    # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        context = 'You are an AI educator which scrapes the pdf from the link given and provides the response to the users question in 500 words with additional links and resources for the users question. If the user asks for a flowchart give a flowchart with explanation'
        convo.send_message(f"{context} Link:{url}, User Question : {user_input}")
        result = convo.last.text
        return render(request, 'resources/roadmap.html', {'result': result,'url' : url})
    return render(request, 'resources/roadmap.html', {'url' : url})
