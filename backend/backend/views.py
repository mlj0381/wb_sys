from django.http import HttpResponse
from django.shortcuts import render


def admin(request):
    return render(request,'index.html')


def head(request):
    return render(request,'pages/home.html')

def hotsport(request):
    return render(request,'pages/hotspot.html')

def analysis(request):
    return render(request,'pages/analysis.html')

def testing(request):
    return render(request,'pages/testing.html')

def view(request):
    return render(request,'pages/view.html')

def task(request):
    return render(request,'pages/task.html')

def task2(request):
    return render(request,'pages/task2.html')

def perinfo(request):
    return render(request,'pages/perinfo.html')