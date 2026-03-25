from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book', 'user', 'plated_end_at', 'end_at']
        labels = {
            'book': 'Книга',
            'user': 'Користувач',
            'plated_end_at': 'Планова дата повернення',
            'end_at': 'Фактична дата повернення'
        }
        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'plated_end_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }