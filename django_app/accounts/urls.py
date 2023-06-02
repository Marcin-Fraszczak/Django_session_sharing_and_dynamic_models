from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('accounts/register/', views.RegisterView.as_view(), name='register'),
	path('accounts/login/', views.LoginView.as_view(), name='login'),
	path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
]
