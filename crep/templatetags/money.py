# coding: utf8
from django import template
from crep.money import money_format

register = template.Library()

register.filter("money_format", money_format)
