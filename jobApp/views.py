from django.shortcuts import render

# Create your views here.
def getjob(request):
    #write job code here
    return render(request,'jobs/job.html')