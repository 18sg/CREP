from django.conf.urls.defaults import *

urlpatterns = patterns("crep.views",
	(r'^$', "index"),
	(r'^transfer/add/$', "add_transfer"),
	(r'^transfer/(?P<id>\d+)/cancel/$', "cancel_transfer"),
	(r'^transfer/(?P<id>\d+)/confirm/$', "confirm_transfer"),
	(r'^user/(?P<username>\w+)/$', "user"),
	(r'^purchase/add/$', "purchase_add"),
	(r'^purchase/add/submit/$', "purchase_add_submit"),
	(r'^purchase/(?P<id>\d+)/$', "purchase"),
	(r'^optimal_transfers/$', "optimal_transfers"),
	(r'^email/$', "email"),
)
