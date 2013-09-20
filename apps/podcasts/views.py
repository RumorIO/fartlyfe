from django.shortcuts import render_to_response
from django.views.generic import ListView, DetailView

from apps.myresume.models import ResumeItem, ResumeProject
from apps.myresume.settings import SKILL_CHOICES


class SkillListView(ListView):
    queryset = [[skill[0],skill[1]] for skill in SKILL_CHOICES]
    template_name = 'myresume/skill_list.html'
    context_object_name = 'skills'

class ProjectListView(ListView):
    template_name = 'myresume/project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        return ResumeProject.objects.filter(skill=self.kwargs['skill'])

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data( **kwargs)
        context['skills']= SKILL_CHOICES
        return context

class ResumeItemListView(ListView):
    template_name = 'myresume/resume_item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        return ResumeItem.objects.filter(project__slug=self.kwargs['project'])

    def get_context_data(self, **kwargs):
        context = super(ResumeItemListView, self).get_context_data( **kwargs)
        context['skills']= SKILL_CHOICES
        return context

class ResumeItemDetailView(DetailView):
    template_name = 'myresume/resume_item_detail.html'
    context_objects_name = 'item'
    model = ResumeItem
