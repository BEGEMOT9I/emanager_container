from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .forms import UserChangeForm, UserCreationForm

from .models import Event, MyUser, Comment, Organization


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('username', 'email', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('email',)}),
		('Permissions', {'fields': ('is_admin',)}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2')}
		),
	)
	search_fields = ('username',)
	ordering = ('username',)
	filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Comment)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)