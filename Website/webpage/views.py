from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def charts(request):
    return render(request, 'charts.html', {})

