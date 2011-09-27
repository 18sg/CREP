from crep.money import money_format

class TransactionFormatMixin(object):
	"""Formatting methods for any class that looks like a transaction."""
	
	def format_sender(self):
		return u"%s to %s" % (money_format(self.ammount), self.recipient.name)
	
	def format_receiver(self):
		return u"%s from %s" % (money_format(self.ammount), self.sender.name)
	
	def __unicode__(self):
		return u"%s from %s to %s" % (money_format(self.ammount),
		                              self.sender.name,
		                              self.recipient.name)
