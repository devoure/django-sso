from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')


def showdate(request):
    return HttpResponse("Todays Date: 21st Feb 2024")
