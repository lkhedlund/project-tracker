from django import forms
from .models import Project, Count

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'total_count', 'start_date', 'end_date',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mdl-textfield__input',
                'id': 'project-title',
                'required': True,
                }),
            'description': forms.Textarea(attrs={
                'class': 'mdl-textfield__input',
                'id': 'project-description',
                'required': True,
                }),
            'total_count': forms.NumberInput(attrs={
                'class': 'mdl-textfield__input',
                'id': 'project-total-count',
                'required': True,
                }),
            'start_date': forms.DateInput(attrs={
                'class': 'mdl-textfield__input',
                'id': 'project-start-date',
                'required': True,
                }),
            'end_date': forms.DateInput(attrs={
                'class': 'mdl-textfield__input',
                'id': 'project-end-date',
                'required': True,
                }),
        }

class CountForm(forms.ModelForm):
    class Meta:
        model = Count
        fields = ('count_update',)
        widgets = {
            'count_update': forms.NumberInput(attrs={
                'class': 'mdl-textfield__input',
                'required': True,
            })
        }
