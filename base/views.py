from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .models import Contact
from .forms import ContactForm

from books.views import BaseMixin


class ContactView(BaseMixin, CreateView):
    model = Contact
    form_class = ContactForm
    queryset = Contact.objects.none()
    template_name = 'base/contact.html'
    success_url = reverse_lazy('contact')


class TermAndConditionView(BaseMixin, TemplateView):
    template_name = 'base/term.html'