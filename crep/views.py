from mt import optimise
from django.http import HttpResponse
from django.core.context_processors import csrf
from mt.crep.models import *
from django.shortcuts import render_to_response, get_object_or_404
import math
from decimal import Decimal

def index(request):
	return render_to_response("crep/index.html", {})


def user(request, username):
	user = User.objects.get(username=username)
	return HttpResponse("User: %s" % len(user.transactions_sent.all()))


def purchase(request, id):
	purchase = get_object_or_404(Purchase, id=id)
	return HttpResponse(repr(dir(purchase)))


def purchase_add(request):
	users = UserProfile.objects.all()
	c = dict(users=users)
	c.update(csrf(request))
	return render_to_response("crep/add_purchase.html", c)


def purchase_add_submit(request):
	purchase = Purchase(title=request.POST["title"],
	                    description=request.POST["description"],
	                    purchaser=UserProfile.objects.get(id=int(request.POST["purchaser"])))
	purchase.save()
	for user in UserProfile.objects.all():
		ammount = int(Decimal(request.POST["w_%s_t" % user.id]) * 100)
		ao = AmmountOwed(user=user, purchase=purchase, ammount=ammount)
		ao.save()
	return HttpResponse("Done!")

def optimal_transfers(request):
	users = UserProfile.objects.all()
	transfers = optimise.optimise_transfers([(u, u.ammount_owed) for u in users])
	return render_to_response("crep/optimal_transfers.html",
	                          dict(transfers=[(t[0], t[1], money_format(t[2]))
	                               for t in transfers]))

