from django.db import models
from django.core.exceptions import ObjectDoesNotExist

import cPickle as pickle

class Variable(models.Model):
	
	key = models.CharField(max_length=30, primary_key=True)
	pickle_value = models.TextField()
	
	@property
	def value(self):
		return pickle.loads(str(self.pickle_value))
	
	@value.setter
	def value(self, value):
		self.pickle_value = pickle.dumps(value)
	
	@classmethod
	def get(klass, key, default=None):
		try:
			return klass.objects.get(key=key).value
		except ObjectDoesNotExist:
			return default
	
	@classmethod
	def set(klass, key, value):
		var = klass.objects.get_or_create(key=key)[0]
		var.value = value
		var.save()
	
	@classmethod
	def delete(klass, key):
		klass.objects.get(key=key).delete()
	
	def __unicode__(self):
		return "%s = %s" % (self.key, self.value)
	
	class Meta:
		app_label="crep"
