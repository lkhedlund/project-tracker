from .models import Project

def recent_projects(request):
    return {'recent_projects': Project.objects.filter(archived=False)[:10]}
