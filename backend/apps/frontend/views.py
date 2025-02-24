from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView


def home(request):
    template_name = 'index.html'
    return render(request, "index.html")

