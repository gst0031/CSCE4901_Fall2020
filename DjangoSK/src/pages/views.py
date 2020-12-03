from django.http import HttpResponse # needed for html code
from django.shortcuts import render

# Create your views here.
def home_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Hello World!</h1>")
    return render(request, "home.html", {})

def contact_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Contact Us:</h1>")
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    #return HttpResponse("<h1>About this project:</h1>")
    return render(request, "about.html", {})

def guides_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Guides</h1>")
    return render(request, "guides.html", {})

def graphs_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Graphs Page!</h1>")
    return render(request, "graphs.html", {})
    
def account_view(request, *args, **kwargs):
    #return HttpResponse("<h1>Accounts</h1>")
    return render(request, "account.html", {})