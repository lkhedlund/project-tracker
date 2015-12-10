from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Count

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project_list.html', { 'projects': projects })

@login_required
def project_detail(request, pk):
    pass

@login_required
def project_new(request):
    pass

@login_required
def project_edit(request, pk):
    pass
