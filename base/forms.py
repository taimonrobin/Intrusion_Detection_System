from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

class UniqueSourceAddrForm(forms.Form):
    address         = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    tolerence_level = forms.DecimalField(max_digits=3, decimal_places=2, validators=[
            MaxValueValidator(3.5),
            MinValueValidator(0.5)
        ])
