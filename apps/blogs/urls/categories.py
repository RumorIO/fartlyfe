from django.conf.urls import patterns, include, url

from apps.blogs.models import Category
from apps.blogs.views import AllCategoryView, ByCategoryView

urlpatterns = patterns('',
    url(r'^$', AllCategoryView.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', ByCategoryView.as_view()),
)
