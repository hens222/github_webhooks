from django.urls import path
from .views import webhook_handler

urlpatterns = [
    path('webhook/', webhook_handler, name='webhook_handler'),

]
