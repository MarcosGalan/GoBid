from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView

from .models import Event  # Update with the actual path to your Event model


class EventListView(ListView):
    model = Event
    template_name = 'events.html'
    context_object_name = 'events'
    queryset = Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            events = Event.objects.all()
        except Event.DoesNotExist:
            # Handle the case when no events are found
            events = []

        context['events'] = events
        return context
