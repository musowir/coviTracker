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
from admin_management import views

urlpatterns = [
    path('instituition-list/', views.InstituitionList.as_view(), name="InstituitionList"),
    path('covid-positive-list/', views.PositiveUserList.as_view(), name="PositiveUserList"),
    path('user-list/', views.UserList.as_view(), name="UserList"),
    path('feedback-list/', views.FeedbackList.as_view(), name="FeedbackList"),
    path('verify/<int:pk>/', views.InstituitionVerification.as_view(), name="InstituitionVerification"),
    path('covid-history/<int:pk>/', views.UserCovidHistoryList.as_view(), name="UserCovidHistoryList"),
    path('change-covid-status/<int:pk>/', views.ChangeCovidStatus.as_view(), name="ChangeCovidStatus"),
    path('visited-users-list/<int:pk>/', views.VisitedUserList.as_view(), name="VisitedUserList"),
    path('', views.Login.as_view(), name="Login"),
]
