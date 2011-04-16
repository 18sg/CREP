# coding: utf8
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.core.signals import request_started
from django.dispatch import receiver
from django.contrib.auth.models import User
import optimise
from crep.money import money_format
import json


class Variable(models.Model):
	
	key = models.CharField(max_length=30, primary_key=True)
	value = models.TextField()
	
	@classmethod
	def get(klass, key, default=None):
		try:
			return json.loads(klass.objects.get(key=key).value)
		except ObjectDoesNotExist:
			return default
	
	@classmethod
	def set(klass, key, value):
		var = klass.objects.get_or_create(key=key)[0]
		var.value = json.dumps(value)
		var.save()
	
	@classmethod
	def delete(klass, key):
		klass.objects.get(key=key).delete()
	
	def __unicode__(self):
		return "%s = %s" % (self.key, json.loads(self.value))


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


def user_post_save(sender, instance, signal, *args, **kwargs):
	profile, new = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)



class Transaction(models.Model):
	sender = models.ForeignKey(UserProfile, 
	                           related_name="transactions_sent")
	recipient = models.ForeignKey(UserProfile, 
	                              related_name="transactions_recieved")
	sent = models.BooleanField()
	recieved = models.BooleanField()
	ammount = models.IntegerField()
	
	def __unicode__(self):
		return u"%s from %s to %s" % (money_format(self.ammount),
		                              self.sender.name,
		                              self.recipient.name)


class TransactionCache(models.Model):
	sender = models.ForeignKey(UserProfile, 
	                           related_name="transaction_cache_sent")
	recipient = models.ForeignKey(UserProfile, 
	                              related_name="transaction_cache_recieved")
	ammount = models.IntegerField()
	
	@classmethod
	def set_dirty(klass, *args, **kwargs):
		Variable.set("transaction_cache_dirty", True)
	
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
		
	
	@receiver(request_started)
	def regen_if_dirty(sender, **kwargs):
		# Guard against cuncurrent access by regenerating again.
		while Variable.get("transaction_cache_dirty", True):
			Variable.set("transaction_cache_dirty", False)
			TransactionCache.regenerate()
	
	
	def __unicode__(self):
		return u"%s from %s to %s" % (money_format(self.ammount),
		                              self.sender.name,
		                              self.recipient.name)


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



class AmmountOwed(models.Model):
	purchase = models.ForeignKey(Purchase, related_name="ammounts")
	user = models.ForeignKey(UserProfile, related_name="ammounts_owed")
	ammount = models.IntegerField()
	
	
	def __unicode__(self):
		return u"%s owes %s for '%s'" % (self.user, money_format(self.ammount), self.purchase)


for c in [Transaction, Purchase, AmmountOwed, UserProfile]:
	models.signals.post_save.connect(TransactionCache.set_dirty, sender=c)
	models.signals.post_delete.connect(TransactionCache.set_dirty, sender=c)



