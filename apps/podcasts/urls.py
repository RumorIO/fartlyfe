from django.conf.urls.defaults import *

from apps.myresume.views import SkillListView, ProjectListView, ResumeItemListView, ResumeItemDetailView

urlpatterns = patterns('',

    url('^$', SkillListView.as_view(), name='skill_list'),
    url('^(?P<skill>[-\w]+)/$', ProjectListView.as_view(), name='project_list'),
    url('^(?P<skill>[-\w]+)/(?P<project>[-\w]+)/$', ResumeItemListView.as_view(), name='resume_project'),
    url('^(?P<skill>[-\w]+)/(?P<project>[-\w]+)/(?P<slug>[-\w]+)/$', ResumeItemDetailView.as_view(), name='resume_item_detail'),
 
)


