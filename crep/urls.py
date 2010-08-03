from django.conf.urls.defaults import *

urlpatterns = patterns("mt.crep.views",
	(r'^$', "index"),
	(r'^user/(?P<username>\w+)/$', "user"),
	(r'^purchase/add/$', "purchase_add"),
	(r'^purchase/(?P<id>\d+)/$', "purchase"),
	(r'^optimal_transfers/$', "optimal_transfers")
)
