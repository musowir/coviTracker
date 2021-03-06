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
from usermanagement import views

urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name="UserRegistration"),
    path('user-check/', views.UserExists.as_view(), name="UserExists"),
    path('profile/<int:pk>/', views.UpdateUserProfile.as_view(), name="UpdateUserProfile"),
    path('feedback/', views.CreateFeedack.as_view(), name="CreateFeedack"),
    path('login/', views.UserLoginAPIView.as_view(), name="UserLoginAPIView"),
    path('change-covid-status/<int:pk>/', views.ChangeCovidStatus.as_view(), name="ChangeCovidStatus"),
]
