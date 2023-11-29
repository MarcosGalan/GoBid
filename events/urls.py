from django.views.generic import TemplateView, ListView, DetailView

from django.urls import path
from .views import EventListView

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
]
