from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    queryset = Contact.objects.none()
    template_name = 'base/contact.html'
    success_url = reverse_lazy('contact')