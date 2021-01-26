from django import forms
from .models import Review, CheckoutAddress


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)


class CheckoutAddressForm(forms.ModelForm):
    class Meta:
        model = CheckoutAddress
        fields = ('city','street','phone_number')

