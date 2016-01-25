from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum
from .models import Project, Count
from .forms import ProjectForm, CountForm

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'tracker/project_list.html', {
        'projects': projects
        })

@login_required
def project_detail(request, pk):
    projects = Project.objects.all()
    project = get_object_or_404(Project, pk=pk)
    counts = project.counts.all()
    count_sum = project.counts.aggregate(Sum('count_update'))
    if request.method == "POST":
        form = CountForm(request.POST)
        if form.is_valid():
            count = form.save(commit=False)
            count.project = project
            count.save()
            return HttpResponseRedirect(reverse('tracker.views.project_detail', args=(project.id,)))
    else:
        form = CountForm()
    return render(request, 'tracker/project_detail.html', {
        'projects': projects,
        'project': project,
        'counts': counts,
        'count_sum': count_sum,
        'form': form
        })

@login_required
def project_new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'tracker/project_edit.html', {
        'form': form
        })

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm( request.POST, instance=project )
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect( 'project_detail', pk=project.pk )
    else:
        form = PostForm( instance=project )
    return render(request, 'tracker/project_edit.html', {
        'form': form
        })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')
