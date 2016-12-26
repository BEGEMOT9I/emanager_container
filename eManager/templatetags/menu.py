from django import template

register = template.Library()
@register.inclusion_tag('eManager/partials/menu.html')
def menu():
	return