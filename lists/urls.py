from django.conf.urls import url
from django.views.generic import TemplateView

from lists.views import TodoList, ListDetail

urlpatterns = [
    # api
    url(r'^$', TodoList.as_view(), name="todo_list"),
    url(r'^(?P<pk>[0-9]+)/$', ListDetail.as_view(), name="list_detail")
]