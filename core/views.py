from django.shortcuts import render
from complaints.models import Complaint
from django.http import HttpResponse
def index(request):
    return render(request, 'index.html')

#def citizen_home(request):
    return render(request, 'citizen/home.html')

def citizen_home(request):
    return HttpResponse("Citizen OK")

def service1_home(request):

    complaints = Complaint.objects.filter(
        assigned_to='roads'
    ).order_by('-created_at')

    return render(request, 'service1/home.html', {
        'complaints': complaints
    })

def service2_home(request):

    complaints = Complaint.objects.filter(
        assigned_to='sanitation'
    ).order_by('-created_at')

    return render(request, 'service2/home.html', {
        'complaints': complaints
    })

def service3_home(request):

    complaints = Complaint.objects.filter(
        assigned_to='electricity'
    ).order_by('-created_at')

    return render(request, 'service3/home.html', {
        'complaints': complaints
    })

def authorities_home(request):
    return render(request, 'dashboard/home.html')