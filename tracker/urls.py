from django.conf.urls import url
from . import views
from tracker.views import ProjectView

urlpatterns = [
    url(r'^$', ProjectView.as_view(), name="project_list"),
    url(r'^project/(?P<pk>[0-9]+)/$', views.project_detail, name="project_detail"),
    url(r'^project/new/$', views.project_new, name="project_new"),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', views.project_edit, name="project_edit"),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.project_delete, name="project_delete"),
]
