from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.process_pdf, name='process_pdf'),
    path('query', views.search_query, name='search_query'),
]