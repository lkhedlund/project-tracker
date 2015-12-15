from django import forms
from .models import Project, Count

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'total_count', 'start_date', 'end_date',)
        widgets = {
            'title': forms.TextInput(attrs={ 'required': True, 'placeholder': 'Title...' } ),
            'description': forms.Textarea(attrs={ 'required': True, 'placeholder': 'Tell us about your project...' } ),
            'total_count': forms.NumberInput(attrs={ 'required': True } ),
            'start_date': forms.DateInput(attrs={ 'required': True } ),
            'end_date': forms.DateInput(attrs={ 'required': True } ),
        }

class CountForm(forms.ModelForm):
    class Meta:
        model = Count
        fields = ('count_update',)
