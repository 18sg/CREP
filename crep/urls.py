from django.conf.urls.defaults import *

urlpatterns = patterns("mt.crep.views",
	(r'^$', "index"),
	(r'^add_transfer/$', "add_transfer"),
	(r'^cancel_transfer$', "cancel_transfer"),
	(r'^confirm_transfer$', "confirm_transfer"),
	(r'^user/(?P<username>\w+)/$', "user"),
	(r'^purchase/add/$', "purchase_add"),
	(r'^purchase/add/submit/$', "purchase_add_submit"),
	(r'^purchase/(?P<id>\d+)/$', "purchase"),
	(r'^optimal_transfers/$', "optimal_transfers")
)
