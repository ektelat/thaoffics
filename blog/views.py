from django.shortcuts import render

from .models import BlogPost


# Create your views here.
def home(request):
    return  render(request,'home.html',{'posts':BlogPost.objects.all()})