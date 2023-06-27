from django.http import HttpResponse
# from django import render

def index(request):
    return HttpResponse("Hello, world.you are at the polls index.")