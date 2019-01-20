from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_link_page', views.input_link_page),
    path('article/<slug:slug>', views.article_page2, name='article_page')
 ]