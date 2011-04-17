# coding: utf8
from django import template

import time

register = template.Library()

@register.filter
def strftime(value, arg):
	return time.strftime(arg, value)
