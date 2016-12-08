from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from lists.models import List, Item
from lists.serializers import TodoListSerializer, ItemSerializer

class TodoList(APIView):
    """
    List all, or create a new one.
    """
    def get(self, request, format=None):
		todo_list = get_list_or_404(List)
		serializer = TodoListSerializer(todo_list, many=True, context={'request':request})
		return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TodoListSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListDetail(APIView):
    """
    Retrieve, update or delete a instance.
    """
    def get_object(self, pk):
        return get_object_or_404(List, pk=pk)

    def get(self, request, pk, format=None):
		todo_list = self.get_object(pk)
		serializer = TodoListSerializer(todo_list, context={'request':request})
		return Response(serializer.data)

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