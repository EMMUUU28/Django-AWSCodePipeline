# RoadMMap
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import requests
from django.shortcuts import render
import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))

def downloadroadmap(request):

    url = 'https://roadmap.sh/pdfs/roadmaps/python.pdf'
    response = requests.get(url)
    print("hello")
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


#resumeAssistant

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_conversational_chain():

    prompt_template = """
    You are a Resume Builder tool, scrape the whole resume and grade the resume out of 100. Mention the Job Description for which the resume is most suitable for as "Job Description:" . Answer the question asked by the users. Dont use bold texts in your answer \n\n
    Resume:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def replace_newlines_with_br(text):
    return text.replace('\n', '**')

def resumeassistant(request):
    if request.method == 'POST' and request.FILES.get('pdf_files'):
        pdf_docs = request.FILES.getlist('pdf_files')
        user_question = request.POST.get('user_question')

        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        result = user_input(user_question)
        print(result)
        final_result = result['output_text']
        return render(request,'resources/resume.html',{'response_text':final_result})
    return render(request,'resources/resume.html')