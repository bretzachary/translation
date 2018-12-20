from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_link_page', views.input_link_page),
 ]