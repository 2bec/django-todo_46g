from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from lists.views import TodoList, ListDetail, TaskDetail

urlpatterns = [
    # api
    url(r'^$', cache_page(60 * 12)(TodoList.as_view()), name="todo_list"),
    url(r'^(?P<pk>[0-9]+)/$', cache_page(60 * 12)(ListDetail.as_view()), name="list_detail"),
    url(r'^task/(?P<pk>[0-9]+)/$', cache_page(60 * 12)(TaskDetail.as_view()), name="task_detail"),
]