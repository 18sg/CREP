# coding: utf8
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	
	user = models.ForeignKey(User, unique=True)
	
	
	@property
	def name(self):
		return self.user.username
	
	
	@property
	def ammount_owed(self):
		return (sum(p.total for p in self.purchases.all()) 
		        - sum(a.ammount for a in self.ammounts_owed.all())) 
	
	
	@property
	def ammount_owed_current(self):
		return (self.ammount_owed 
		        - sum(t.ammount for t in self.transactions_recieved.all())
		        + sum(t.ammount for t in self.transactions_sent.all()))
	
	
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
	ammount = models.DecimalField(max_digits=6, decimal_places=2)
	
	def __unicode__(self):
		return u"£%d from %s to %s" % (self.ammount,
		                               self.sender.name,
		                               self.recipient.name)



class Purchase(models.Model):
	purchaser = models.ForeignKey(UserProfile, related_name="purchases")
	title = models.CharField(max_length=200)
	description = models.TextField()
	
	@property
	def total(self):
		return sum(ammount.ammount for ammount in self.ammounts.all())
	
	def __unicode__(self):
		return u"%s for £%s by %s" % (self.title, self.total, self.purchaser.name)



class AmmountOwed(models.Model):
	purchase = models.ForeignKey(Purchase, related_name="ammounts")
	user = models.ForeignKey(UserProfile, related_name="ammounts_owed")
	ammount = models.DecimalField(max_digits=6, decimal_places=2)
	
	
	def __unicode__(self):
		return u"%s owes £%s for '%s'" % (self.user, self.ammount, self.purchase)
