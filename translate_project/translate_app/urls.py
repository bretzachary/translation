from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_link_page', views.input_link_page),
    path('article/<slug:slug>', views.article_page_with_paywall, name='article_page'),
#   path('section/<section:section>', views.section_page, name='section_page'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('restricted', views.restricted, name='restricted'),
    path('user_page', views.user_page, name='user_page'),
    path('section/<str:section>', views.section_page, name='section_page'),
    #path('goto', views.track_article_pageviews, name='track_article_pageviews'),
 ]