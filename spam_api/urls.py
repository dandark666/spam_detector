from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_status, name='api_status'),
    path('metrics/', views.get_metrics, name='get_metrics'),
    path('predict/', views.predict_spam, name='predict_spam'),
]
