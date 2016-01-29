from django.conf.urls import url
from . import views
from tracker.views import ProjectList, ProjectDetail, ProjectNew, ProjectEdit

urlpatterns = [
    url(r'^$', ProjectList.as_view(), name="project_list"),
    url(r'^project/(?P<pk>[0-9]+)/$', ProjectDetail.as_view(), name="project_detail"),
    url(r'^project/new/$', ProjectNew.as_view(), name="project_new"),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', ProjectEdit.as_view(), name="project_edit"),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.project_delete, name="project_delete"),
]
