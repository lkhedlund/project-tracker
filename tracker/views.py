from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.db.models import Sum
import datetime
from .models import Project, Count
from .forms import ProjectForm, CountForm

@method_decorator(login_required, name='dispatch')
class ProjectView(View):

    def get(self, request):
        projects = Project.objects.all()
        return render(request, 'tracker/project_list.html', {
            'projects': projects
            })

@login_required
def project_detail(request, pk):
    # FIXME: Need to refactor into Class-based views
    projects = Project.objects.all()
    project = get_object_or_404(Project, pk=pk)
    counts = project.counts.all()
    count_sum = project.counts.aggregate(Sum('count_update'))
    # Variables for date_progress and words_per_day
    sum_value = next(iter(count_sum.values()))
    if sum_value == None:
        sum_value = 0
    remaining_words = project.total_count - sum_value
    remaining_days = (project.end_date - datetime.date.today()).days
    time_from_start = (datetime.date.today() - project.start_date).days
    total_days = (project.end_date - project.start_date).days
    try:
        words_per_day = int(remaining_words / remaining_days)
    except ZeroDivisionError:
        words_per_day = int(remaining_words)
    try:
        date_progress = (time_from_start / total_days) * 100
    except ZeroDivisionError:
        # If the remaining days is 0, then we want the bar to be full
        date_progress = 100
    if request.method == "POST":
        form = CountForm(request.POST)
        if form.is_valid():
            count = form.save(commit=False)
            count.project = project
            count.save()
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
    else:
        form = CountForm()
    return render(request, 'tracker/project_detail.html', {
        'projects': projects,
        'project': project,
        'counts': counts,
        'count_sum': count_sum,
        'date_progress': date_progress,
        'words_per_day': words_per_day,
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
        form = ProjectForm( instance=project )
    return render(request, 'tracker/project_edit.html', {
        'form': form
        })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')
