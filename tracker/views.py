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
class ProjectList(View):
    template_name = 'tracker/project_list.html'

    def get(self, request):
        projects = Project.objects.all()
        return render(request, self.template_name, {
            'projects': projects
            })

@method_decorator(login_required, name='dispatch')
class ProjectDetail(View):
    form_class = CountForm
    template_name = 'tracker/project_detail.html'

    def get(self, request, pk):
        form = self.form_class
        project = get_object_or_404(Project, pk=pk)
        counts = project.counts.all()
        count_sum = project.counts.aggregate(Sum('count_update'))
        sum_value = self.__sum_value(count_sum)
        date_progress = self.__date_progress(project)
        words_per_day = self.__words_per_day(project, sum_value)
        # Variables for date_progress and words_per_day
        return render(request, self.template_name, {
            'project': project,
            'counts': counts,
            'count_sum': count_sum,
            'date_progress': date_progress,
            'words_per_day': words_per_day,
            'form': form
            })

    def post(self, request, pk):
        form = self.form_class(request.POST)
        project = get_object_or_404(Project, pk=pk)
        counts = project.counts.all()
        count_sum = project.counts.aggregate(Sum('count_update'))
        sum_value = self.__sum_value(count_sum)
        date_progress = self.__date_progress(project)
        words_per_day = self.__words_per_day(project, sum_value)
        if form.is_valid():
            count = form.save(commit=False)
            count.project = project
            print(count_sum)
            count.count_update = self.__count_diff(form.cleaned_data['count_update'], count_sum['count_update__sum'])
            count.save()
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        return render(request, self.template_name, {
            'project': project,
            'counts': counts,
            'count_sum': count_sum,
            'date_progress': date_progress,
            'words_per_day': words_per_day,
            'form': form
            })

    def __words_per_day(self, project, sum_value):
        remaining_words = project.total_count - sum_value
        remaining_days = (project.end_date - datetime.date.today()).days
        try:
            return int(remaining_words / remaining_days)
        except ZeroDivisionError:
            return int(remaining_words)

    def __date_progress(self, project):
        time_from_start = (datetime.date.today() - project.start_date).days
        total_days = (project.end_date - project.start_date).days
        try:
            return (time_from_start / total_days) * 100
        except ZeroDivisionError:
            # If the remaining days is 0, then we want the bar to be full
            return 100

    def __sum_value(self, count_sum):
        # Return the value of count_sum or 0 if None.
        return next(iter(count_sum.values())) or 0

    def __count_diff(self, data, count_sum):
        # Returns the difference between the data and the sum if the new value
        # is greater. This is meant to account for someone updating their count
        # from a total count (like word count from MS Word).
        print(data, count_sum)
        if data > -1:
            return data - count_sum
        else:
            return data

@method_decorator(login_required, name='dispatch')
class ProjectNew(View):
    form_class = ProjectForm
    template_name = 'tracker/project_edit.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {
            'form': form
            })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect('project_detail', pk=project.pk)
        return render(request, self.template_name, {
            'form': form
            })

@method_decorator(login_required, name='dispatch')
class ProjectEdit(View):
    form_class = ProjectForm
    template_name = 'tracker/project_edit.html'

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = self.form_class( instance=project )
        return render(request, self.template_name, {
            'form': form
            })

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = self.form_class( request.POST, instance=project )
        if form.is_valid():
            project = form.save(commit=False)
            project.user_id = request.user
            project.save()
            return redirect( 'project_detail', pk=project.pk )
        return render(request, 'tracker/project_edit.html', {
            'form': form
            })

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')
