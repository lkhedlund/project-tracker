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
class ArchiveList(View):
    template_name ="tracker/archive_list.html"

    def get(self, request):
        archived_projects = Project.objects.filter(archived=True).order_by('start_date')
        return render(request, self.template_name, {
            'archived_projects': archived_projects,
            })

@method_decorator(login_required, name='dispatch')
class ProjectList(View):
    template_name = 'tracker/project_list.html'

    def get(self, request):
        projects = Project.objects.filter(archived=False).order_by('end_date')[:10]
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
        total_days = (project.end_date - project.start_date).days
        sum_value = self.__sum_value(count_sum)
        date_progress = self.__date_progress(project, total_days)
        words_per_day = self.__words_per_day(project, sum_value)
        counts_today = self.__count_by_day(counts, datetime.date.today())
        daily_counts_array = self.__linear_count_chart(project, counts)
        # Variables for date_progress and words_per_day
        return render(request, self.template_name, {
            'project': project,
            'counts': counts,
            'count_sum': count_sum,
            'date_progress': date_progress,
            'words_per_day': words_per_day,
            'counts_today': counts_today,
            'total_days': total_days,
            'daily_counts_array': daily_counts_array,
            'form': form
            })

    def post(self, request, pk):
        form = self.form_class(request.POST)
        project = get_object_or_404(Project, pk=pk)
        counts = project.counts.all()
        count_sum = project.counts.aggregate(Sum('count_update'))
        sum_value = self.__sum_value(count_sum)
        if form.is_valid():
            count = form.save(commit=False)
            count.project = project
            count.count_update = self.__count_diff(form.cleaned_data['count_update'], sum_value)
            count.save()
            return HttpResponseRedirect(reverse('project_detail', args=(project.id,)))
        return render(request, self.template_name, {
            'form': form
            })

    def __words_per_day(self, project, sum_value):
        remaining_words = project.total_count - sum_value
        remaining_days = (project.end_date - datetime.date.today()).days
        try:
            return int(remaining_words / remaining_days)
        except ZeroDivisionError:
            return int(remaining_words)

    def __date_progress(self, project, total_days):
        time_from_start = (datetime.date.today() - project.start_date).days
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
        if data > -1:
            return data - count_sum
        else:
            return data

    def __date_range(self, start_date, end_date):
        # Returns every date in the range
        return (start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1))

    def __count_by_day(self, counts, date):
        # Returns the count on a given day
        return counts.filter(created_date=date).aggregate(Sum('count_update'))

    def __linear_count_chart(self, project, counts):
        # Returns an array with data that is useable by google charts
        array = [['Day', 'Count']]
        for date in self.__date_range(project.start_date, datetime.date.today()):
            day = (date - project.start_date).days
            count = self.__count_by_day(counts, date)
            count = self.__sum_value(count)
            array.append([day, count])
        return array

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
    if project.user_id == request.user:
        project.delete()
    return redirect('project_list')

@login_required
def project_archive(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.archived:
        project.archived = False
    else:
        project.archived = True
    project.save()
    return redirect('project_list')
