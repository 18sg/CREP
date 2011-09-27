# coding: utf8
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import User

from crep.money import money_format
from crep.models.transaction import TransactionFormatMixin


class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	
	
	@property
	def name(self):
		return self.user.first_name or self.user.username
	
	@property
	def ammount_owed(self):
		return (AmmountOwed.objects
		                    .filter(purchase__purchaser=self)
		                    .aggregate(s=Sum("ammount"))["s"]
		        - self.ammounts_owed.aggregate(s=Sum("ammount"))["s"])
	
	@property
	def ammount_owed_current(self):
		return (self.ammount_owed 
		        - self.transactions_recieved.aggregate(s=Sum("ammount"))["s"]
		        + self.transactions_sent.aggregate(s=Sum("ammount"))["s"])
	
	def __unicode__(self):
		return unicode(self.user)
	
	@property
	def status(self):
		ammount_owed = self.ammount_owed_current
		if ammount_owed > 0:
			return u"You are owed %s." % money_format(ammount_owed)
		if ammount_owed < 0:
			return u"You owe %s." % money_format(-ammount_owed)
		else:
			return u"You are even."
	
	class Meta:
		app_label="crep"

@receiver(models.signals.post_save, sender=User)
def make_user_profile(sender, instance, signal, *args, **kwargs):
	profile, new = UserProfile.objects.get_or_create(user=instance)



class Transaction(models.Model, TransactionFormatMixin):
	sender = models.ForeignKey(UserProfile, 
	                           related_name="transactions_sent")
	recipient = models.ForeignKey(UserProfile, 
	                              related_name="transactions_recieved")
	sent = models.BooleanField()
	recieved = models.BooleanField()
	ammount = models.IntegerField()
	
	class Meta:
		app_label="crep"



class Purchase(models.Model):
	purchaser = models.ForeignKey(UserProfile, related_name="purchases")
	title = models.CharField(max_length=200)
	description = models.TextField()
	
	@property
	def total(self):
		return self.ammounts.aggregate(s=Sum("ammount"))["s"]
	
	def __unicode__(self):
		return u"%s for %s by %s" % (self.title,
		                             money_format(self.total),
		                             self.purchaser.name)
	
	class Meta:
		app_label="crep"



class AmmountOwed(models.Model):
	purchase = models.ForeignKey(Purchase, related_name="ammounts")
	user = models.ForeignKey(UserProfile, related_name="ammounts_owed")
	ammount = models.IntegerField()
	
	def __unicode__(self):
		return u"%s owes %s for '%s'" % (self.user, money_format(self.ammount), self.purchase)
	
	class Meta:
		app_label="crep"

