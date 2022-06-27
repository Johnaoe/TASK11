from django import forms
from .models import RepairOrder, Car

class OrderForm(forms.ModelForm):

    class Meta:
        model = RepairOrder
        fields = ('car', 'car_issue', 'due_back')
        widgets = {
            'car': forms.Select(),
            'car_issue': forms.Textarea(attrs={'class': 'form-control'}),
            'due_back': forms.DateInput(),
        }