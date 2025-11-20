from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def settings_page(request):
    return render(request, "settings/settings_page.html")
