from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from .models import Event, EventRegistration
from django.contrib.auth.mixins import LoginRequiredMixin

from books.views import BaseMixin


class EventList(BaseMixin, ListView):
    model = Event
    template_name = 'event/event_list.html'
    queryset = Event.objects.prefetch_related('event_of').all().order_by('-id')
    paginate_by = 12


class EventDetail(BaseMixin, DetailView):
    model = Event
    template_name = 'event/event_detail.html'
    queryset = Event.objects.prefetch_related('event_of').all()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context_data['registered'] = EventRegistration.objects.filter(user=self.request.user, event=self.get_object()).exists()
        return context_data


def event_regiseter(request, slug):
    event = Event.objects.get(slug=slug)
    user = request.user
    EventRegistration.objects.create(event=event, user=user)
    return redirect(request.META.get('HTTP_REFERER'))


