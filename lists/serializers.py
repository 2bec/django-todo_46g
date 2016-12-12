import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from lists.models import List, Item


class UserSerializer(serializers.ModelSerializer):
    
    # add username custom field, to avoid already exists users erros.
    username = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('username',)


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    pk = serializers.IntegerField(read_only=True)

    # use serializer to users
    # required false to permited anonymous users?
    assigned_to = UserSerializer(required=False)
    created_by = UserSerializer(required=False)    

    class Meta:
        model = Item
        fields =  (
            'url',
            'pk',
            'title',
            'priority',
            'assigned_to',
            'created_by',
            'completed',
            'completed_date'
        )
        # explicity custom view_name and lookup_field
        extra_kwargs = {
            'url': {'view_name': 'task_detail', 'lookup_field': 'pk'}
        }


class TodoListSerializer(serializers.HyperlinkedModelSerializer):

    pk = serializers.IntegerField(read_only=True)

    # use serializer to taks
    tasks = ItemSerializer(many=True)

    class Meta:
        model = List
        fields = ('url', 'pk', 'title', 'tasks')
        # explicity custom view_name and lookup_field
        extra_kwargs = {
            'url': {'view_name': 'list_detail', 'lookup_field': 'pk'}
        }

    def create(self, validated_data):
        # get tasks on validated_data
        # and create todo_list with validade_data
        tasks_data = validated_data.pop('tasks')
        todo_list = List.objects.create(**validated_data)

        for t_data in tasks_data:
            # get assigned_to and created_by from t_data
            # than get or create user passing username
            assigned_data = t_data.pop('assigned_to')
            assigned_to, created = User.objects.get_or_create(username=assigned_data["username"])
            created_data = t_data.pop('created_by')
            created_by, created = User.objects.get_or_create(username=created_data["username"])
            # and now create Item (task)
            Item.objects.create(
                todo_list=todo_list,
                assigned_to=assigned_to,
                created_by=created_by,
                **t_data
            )

        return todo_list

    def update(self, instance, validated_data):
        # get taks from validated_data
        tasks_data = validated_data.pop('tasks')
        # mapping
        tasks_mapping = {item['pk']: item for item in tasks_data}

        # update the list instance
        instance.title = validated_data['title']
        instance.save()

        # creations and updates
        for task_id, data in tasks_mapping.items():
            # get assigned_to and created_by from data
            # than get or create user passing username
            assigned_data = data.pop('assigned_to')
            assigned_to, created = User.objects.get_or_create(username=assigned_data["username"])
            created_data = data.pop('created_by')
            created_by, created = User.objects.get_or_create(username=created_data["username"])
            # get or create an Item (task)
            task, created = Item.objects.get_or_create(id=task_id, todo_list=instance)
            # and make any changes or not, dont forgot save()
            task.priority = data.get('priority', task.priority)
            task.assigned_to = assigned_to
            task.created_by = created_by
            task.title = data.get('title', task.title)
            task.save()

        # Delete if necessary
        # for task_id, task in tasks_mapping.items():
        #     if task_id not in instance.tasks.all():
        #         task.delete()

        return instance