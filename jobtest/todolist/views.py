from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from . import models
from .serializers import UserSerializer, GroupSerializer, FullListTODOSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks, or create a new task.
    """
    if request.method == 'GET':
        tasks = models.Item.objects.all()
        serializer = FullListTODOSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FullListTODOSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def status_report(request):
    todo_listing = []

    for todo_list in models.List.objects.all():
        todo_dict = {}

        todo_dict['list_object'] = todo_list

        todo_dict['item_count'] = todo_list.item_set.count()

        todo_dict['items_complete'] = todo_list.item_set.filter(completed=True).count()

        todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)

        todo_listing.append(todo_dict)

    return render_to_response('status_report.html', {'todo_listing': todo_listing})


