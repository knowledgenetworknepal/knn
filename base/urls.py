from django.urls import path

from .views import ContactView, TermAndConditionView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('ternsandconditions/', TermAndConditionView.as_view(), name='terms_and_conditions'),

]