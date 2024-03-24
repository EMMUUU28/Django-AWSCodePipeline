from django.shortcuts import render
from serpapi import GoogleSearch

# Create your views here.
def getjob(request):
    

    params = {
    "engine": "google_jobs",
    "q": "mumbai software developer",
    "hl": "en",
    "num": "25",
    "api_key": "3fb9e0be680fbc384833423e983140627c494f8d1468c6dc9d1282661ede94e6"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_results = results["jobs_results"]
    # print(jobs_results)
    return render(request,'jobs/job.html',{'job_list':jobs_results})