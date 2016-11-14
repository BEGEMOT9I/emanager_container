# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# Create your models here.
@python_2_unicode_compatible
class Event(models.Model):
	
	city = models.CharField(max_length=50, verbose_name='город', default='')
	organizer = models.CharField(max_length=200, verbose_name='организатор', default='')
	name = models.CharField(max_length=1000, verbose_name='название')
	start_date = models.DateTimeField(verbose_name='дата начала')
	description = models.CharField(max_length=1000, verbose_name='описание')
	addres = models.CharField(max_length=200, verbose_name='место проведения', default='')
	image = models.ImageField(upload_to='images', blank=True, verbose_name='постер')

	class Meta:
		verbose_name = 'событие'
		verbose_name_plural = 'события'

	def __str__(self):
		return self.name