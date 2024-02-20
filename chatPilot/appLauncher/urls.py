from django.urls import path
from . import views

urlpatterns = [
    path('process_pdf/', views.process_pdf, name='process_pdf'),
    path('search_query/', views.search_query, name='search_query'),
    
]