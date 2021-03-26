from django.urls import path

from .views import AboutUsView, ContactView, TermAndConditionView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('ternsandconditions/', TermAndConditionView.as_view(), name='terms_and_conditions'),
    path('aboutus/', AboutUsView.as_view(), name='aboutus'),

]