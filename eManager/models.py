# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

class MyUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email or not username:
			raise ValueError('Users must have an email and username address')

		user = self.model(
			username=username,
			email=self.normalize_email(email)
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username, email, password):
		user = self.create_user(
			username,
			email=email,
			password=password
		)

		user.is_admin = True
		user.save(using=self._db)
		return user

@python_2_unicode_compatible
class MyUser(AbstractBaseUser):
	username = models.CharField(
		max_length=150,
		unique=True,
	)
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	class Meta:
		verbose_name = 'пользователь'
		verbose_name_plural = 'пользователи'

@python_2_unicode_compatible
class Event(models.Model):
	
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='пользователи')
	organizer = models.CharField(max_length=200, verbose_name='организатор', default='')
	name = models.CharField(max_length=1000, verbose_name='название')
	start_date = models.DateTimeField(verbose_name='дата начала')
	description = models.CharField(max_length=1000, verbose_name='описание')
	address = models.CharField(max_length=200, verbose_name='место проведения', default='')
	image = models.ImageField(upload_to='images', blank=True, verbose_name='постер')

	class Meta:
		verbose_name = 'событие'
		verbose_name_plural = 'события'

	def __str__(self):
		return self.name

class CommentManager(models.Manager):
	def create_comment(self, event, user, text):
		comment = self.create(
			event=event,
			user=user,
			text=text,
			created_date=timezone.now()
		)

		return comment

@python_2_unicode_compatible
class Comment(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='события')
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='пользователи')
	text = models.TextField()
	created_date = models.DateTimeField(auto_now=True)

	objects = CommentManager()

	def __str__(self):
		return self.text