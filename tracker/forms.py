from django import forms
from .models import Project, Count

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'total_count', 'start_date', 'end_date',)

class CountForm(forms.ModelForm):
    class Meta:
        model = Count
        fields = ('count_update',)
