from django.shortcuts import render
from django.contrib import messages


def index(request):
    messages.success(request, "WAT")
    return render(request, 'home/index.html')
