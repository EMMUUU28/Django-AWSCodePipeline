from django.shortcuts import render,redirect
from django.core import serializers
import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .models import Meeting
load_dotenv()
WHEREBY_API_KEY = os.getenv('WHEREBY_API_KEY')
# Create your views here.
def joincall(request):
    
    

    return render(request,'videocall/mentorconnect.html')

def listrooms(request):

    meetings = Meeting.objects.all()

    print(meetings)
    


    return render(request,'videocall/mentorlist.html',{'meetings':meetings})

def createmeet(request):
        
    if request.method == 'POST':
        host_name = request.POST.get('host_name')
        meet_for = request.POST.get('meet_for')
        description = request.POST.get('description')
        
        # You can process the data further, such as saving it to a database or performing other actions
        
        # For now, let's just print the data
        print(f'Host Name: {host_name}')
        print(f'Meet For: {meet_for}')
        print(f'Description: {description}')
        
        mentorname="Valentine"
        url = "https://api.whereby.dev/v1/meetings"

        date_now = datetime.now()
        two_weeks_future_date = (date_now + timedelta(days=14)).isoformat()

        payload = json.dumps({
        "isLocked": False,
        "roomNamePrefix": mentorname,
        "roomNamePattern": "uuid",
        "roomMode": "normal",
        "endDate": two_weeks_future_date,
        "fields": []
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+ WHEREBY_API_KEY
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)

        # print(response.text)

        meeting = Meeting(
        startDate=data['startDate'],
        endDate=data['endDate'],
        roomName=data['roomName'],
        roomUrl=data['roomUrl'],
        meetingId=data['meetingId'],
        hostname=host_name,
        objective=meet_for
        )
        meeting.save()

        
        # You can also return an HttpResponse or redirect to another page after processing the form data
        return redirect('/mentorlist')
    else:
        # Handle GET request or other methods if needed
        return render(request,'videocall/createcall.html')