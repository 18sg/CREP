# coding: utf8
from decimal import Decimal

def money_format(ammount):
	"""Format an ammount in pence as an ammount in GBP."""
	d = Decimal(ammount)
	return u'£%s' % (d / 100)

def money_parse(ammount):
	"""Convert a string in GBP into a number of pence.
	Rounds down to the nearest penny."""
	return int(Decimal(ammount) * 100)
