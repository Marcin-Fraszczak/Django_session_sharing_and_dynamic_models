from django.urls import path
from . import views

app_name = 'dynamo'

urlpatterns = [
	path('', views.CreateModelView.as_view(), name='create_model'),
	path('list_models/', views.ListModelsView.as_view(), name='list_models'),
]