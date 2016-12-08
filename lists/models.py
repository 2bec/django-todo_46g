from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
	title = models.CharField(max_length=180, unique=True)

	def __str__(self):
		return self.title

	def get_incomplete_itens(self):
		return Item.objects.filter(todo_list=self, completed=None)


class Item(models.Model):
	title = models.CharField(max_length=180)
	todo_list = models.ForeignKey(List, related_name='tasks', on_delete=models.CASCADE)
	assigned_to = models.ForeignKey(User, blank = True, null = True, on_delete=models.CASCADE, related_name='assigned_to')
	priority = models.IntegerField(default=5)
	completed = models.NullBooleanField(default=None)
	completed_date = models.DateTimeField(blank=True, null=True)
	created_on = models.DateTimeField()
	created_by = models.ForeignKey(User, blank = True, null = True, on_delete=models.CASCADE, related_name='created_by')

	class Meta:
		ordering = ['-priority', 'created_on']

	def __str__(self):
		return self.title

	# Set completed
	def save(self, **kwargs):
		if not self.created_on:
			self.created_on = datetime.datetime.now()
		if self.completed:
			self.completed_date = datetime.datetime.now()
		
		super(Item, self).save()



