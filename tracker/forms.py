from django import forms
from .models import Project, Count

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'total_count', 'start_date', 'end_date',)
        widgets = {
            'title': forms.TextInput(attrs={'id': 'project-title', 'required': True, 'placeholder': 'Title...' } ),
            'description': forms.Textarea(attrs={'id': 'project-description', 'required': True, 'placeholder': 'Tell us about your project...' } ),
            'total_count': forms.NumberInput(attrs={'id': 'project-total-count', 'required': True } ),
            'start_date': forms.DateInput(attrs={'id': 'project-start-date', 'required': True } ),
            'end_date': forms.DateInput(attrs={'id': 'project-end-date', 'required': True } ),
        }

class CountForm(forms.ModelForm):
    class Meta:
        model = Count
        fields = ('count_update',)
