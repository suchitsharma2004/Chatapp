# urls.py

from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('inbox/', views.inbox, name='inbox'),
    path('compose/', views.compose, name='compose'),
    path('drafts/', views.drafts, name='drafts'),
    path('sent/', views.sent, name='sent'),
    path('logout/', views.logout_view, name='logout'),
    path('csrf/', get_csrf_token, name='get_csrf_token'),
]
