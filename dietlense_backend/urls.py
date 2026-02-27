"""
URL configuration for dietlense_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from diet_app import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegisterView.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    path('profile/', views.UserProfileCreateView.as_view()),
    path('profile/<int:pk>/', views.UserProfileRetrieveUpdateView.as_view()),
    path('user/<int:pk>/', views.UserRetrieveView.as_view()),
    path('foodlog/', views.FoodLogCreateListView.as_view()),
    path('foodlog/<int:pk>/', views.FoodLogRetrieveUpdateDestroyView.as_view()),
    path('summary/', views.SummaryView.as_view()),
    path('get-diet-plan/', views.GetDietPlan.as_view()),
]
