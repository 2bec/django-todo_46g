from django.conf.urls import url
from django.views.generic import TemplateView

from lists.views import TodoList, ListDetail, TaskDetail

urlpatterns = [
    # api
    url(r'^$', TodoList.as_view(), name="todo_list"),
    url(r'^(?P<pk>[0-9]+)/$', ListDetail.as_view(), name="list_detail"),
    url(r'^task/(?P<pk>[0-9]+)/$', TaskDetail.as_view(), name="task_detail"),
]