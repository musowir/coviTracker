"""COVID_TRACING URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from institutes import views

urlpatterns = [
    path('login/', views.InstituitionLogin.as_view(), name="InstituitionLogin"),
    path('register/', views.InstituteRegistration.as_view(), name="InstituteRegistration"),
    path('profile/<int:pk>/', views.InstituiteProfile.as_view(), name="InstituiteProfile"),
    path('visitors/<int:pk>/', views.VisitedUsersAPI.as_view(), name="VisitedUsersAPI"),
    path('add-visited-users/', views.AddVisitedUsers.as_view(), name="AddVisitedUsers"),
    path('get-list/', views.GetInituitionList.as_view(), name="GetInituitionList"),
    path('send-alert/', views.SendAlert.as_view(), name="SendAlert"),
]
