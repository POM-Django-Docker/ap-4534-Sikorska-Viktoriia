from django import forms
from .models import Book
from author.models import Author

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        label="Автори",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors', 'issue_date']
        labels = {
            'name': 'Назва книги',
            'description': 'Опис',
            'count': 'Кількість',
            'issue_date': 'Дата видання'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть назву'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'count': forms.NumberInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }