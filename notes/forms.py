from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Текст заметки...'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=True,
        label="Поиск",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Что ищем?'})
    )