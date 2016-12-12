from django.shortcuts import get_object_or_404, get_list_or_404
# from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from lists.models import List, Item
from lists.serializers import TodoListSerializer, ItemSerializer

class TodoList(APIView):
    """
    List all, or create a new one.
    API View that returns results from the cache when possible.
    """
    def get(self, request, format=None):
        # # get cache if exists and return
        # todo_data = cache.get('todo_data')
        # # if cache not exists
        # if todo_data is None:
            # Podemos realizar filtos no resultado
        todo_list = get_list_or_404(List)
        serializer = TodoListSerializer(todo_list, many=True, context={'request':request})
        todo_data = serializer.data
        # # set cache with data and expiry time
        # cache.set('todo_data', todo_data, 12*60)
        return Response(todo_data)

    def post(self, request, format=None):
        serializer = TodoListSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(APIView):
    """
    Retrieve, update or delete a instance.
    API View that returns results from the cache when possible.
    """
    def get_object(self, pk):
        return get_object_or_404(List, pk=pk)

    def get(self, request, pk, format=None):
        # get cache if exists and return
        # todo_data = cache.get('todo_detail')
        # # if cache not exists
        # if todo_data is None:
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list, context={'request':request})
        todo_data = serializer.data
        # # set cache with data and expiry time
        # cache.set('todo_detail', todo_data, 12*60)
        return Response(todo_data)

    def put(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        serializer = TodoListSerializer(todo_list, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        todo_list = self.get_object(pk)
        todo_list.delete()
        return Response(todo_list)


class TasksList(APIView):
    """
    List all, or create a new one.
    """
    def get(self, request, format=None):
        # Podemos realizar filtos no resultado
        tasks = get_list_or_404(Item)
        serializer = ItemSerializer(tasks, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ItemSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    """
    Retrieve, update or delete a instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Item, pk=pk)

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = ItemSerializer(task, context={'request':request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = ItemSerializer(task, data=request.data, partial=True, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(task)