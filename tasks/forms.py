from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'due_date', 'category')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Enter task title',
                    'class': 'form-control'
                }
            ),
            'due_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }
