import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
import pandas as pd
from .models import excel

def clusters(request):
    #col_list = ['terms']
    #data = pd.read_csv(r'C:/Users/Greg/Documents/temporal_website/tables/df_summary 1.csv')
    csvDataFile = open(r'C:/Users/Greg/Documents/temporal_website/tables/df_summary 1.csv', 'r')
    data=list(csv.reader(csvDataFile))
    terms = data[2][1]
    #data_html = terms.to_html()
    data2 = pd.read_csv(r'C:/Users/Greg/Documents/temporal_website/tables/bias clustring 1.csv')
    data2_html = data2.to_html()
    context = {'loaded_data':terms,#'loaded_data2':data2_html,#'loaded_data3':terms
               }
    return render(request, "tables/cluster.html", context)

def index(request):
    # Create the HttpResponse object with the appropriate CSV header.
    #response = HttpResponse(content_type='text/csv')
    #response['Content-Disposition'] = 'attachment; filename="Journal_of_Financial_Economics_2020.csv"'

    #csvfile = request.FILES['Journal_of_Financial_Economics_2020.csv']
    data = pd.read_csv(r'C:/Users/Greg/Documents/temporal_website/tables/df_summary 1.csv')
    data_html = data.to_html()
    data2 = pd.read_csv(r'C:/Users/Greg/Documents/temporal_website/tables/bias clustring 1.csv')
    data2_html = data2.to_html()
    context = {'loaded_data':data_html,'loaded_data2':data2_html}
    return render(request, "tables/tables.html", context)


        
