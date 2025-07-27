from django import forms
from .models import Book
from django import forms

class ExampleForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BookSearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Search books...', 'class': 'form-control'})
    )
