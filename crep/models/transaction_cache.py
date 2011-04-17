from django.db import models
from django.core.signals import request_started
from django.dispatch import receiver

from crep.models.core import *
from crep.models.variable import Variable
import optimise


class TransactionCache(models.Model):
	sender = models.ForeignKey(UserProfile, 
	                           related_name="transaction_cache_sent")
	recipient = models.ForeignKey(UserProfile, 
	                              related_name="transaction_cache_recieved")
	ammount = models.IntegerField()
	
	@classmethod
	def regenerate(klass):
		TransactionCache.objects.all().delete()
		users = UserProfile.objects.all()
		transfers = optimise.optimise_transfers([(u, u.ammount_owed_current) for u in users])
		
		for sender, recipient, ammount in transfers:
			t = TransactionCache(sender=sender,
			                      recipient=recipient,
			                      ammount=ammount)
			t.save()
		
	def __unicode__(self):
		return u"%s from %s to %s" % (money_format(self.ammount),
		                              self.sender.name,
		                              self.recipient.name)
	
	class Meta:
		app_label="crep"


def set_dirty(*args, **kwargs):
	Variable.set("transaction_cache_dirty", True)

@receiver(request_started)
def regen_if_dirty(sender, **kwargs):
	# Guard against cuncurrent access by regenerating again.
	while Variable.get("transaction_cache_dirty", True):
		Variable.set("transaction_cache_dirty", False)
		TransactionCache.regenerate()
	
for c in [Transaction, Purchase, AmmountOwed, UserProfile]:
	models.signals.post_save.connect(set_dirty, sender=c)
	models.signals.post_delete.connect(set_dirty, sender=c)
