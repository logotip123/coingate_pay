from django import forms


class PayForm(forms.Form):
    donation = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mr-sm-2',
                                                                  'value': 10
                                                                  }))

