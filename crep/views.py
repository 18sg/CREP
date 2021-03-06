import optimise
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from crep.models import *
from crep.money import money_format, money_parse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user

import time


def get_user_profile(request):
	return UserProfile.objects.get(user=get_user(request))


def return_to_previous(request):
	referer = request.META.get('HTTP_REFERER', None)
	return HttpResponseRedirect(referer or "/crep/")


@login_required
def index(request):
	user = get_user_profile(request)
	from_transfers = Transaction.objects.filter(sender=user, sent=True, recieved=False)
	to_transfers = Transaction.objects.filter(recipient=user, sent=True, recieved=False)
	suggested_from_transfers = TransactionCache.objects.filter(sender=user)
	suggested_to_transfers = TransactionCache.objects.filter(recipient=user)
	
	c = dict(users=UserProfile.objects.all(),
	         user=user,
	         to_transfers=to_transfers,
	         from_transfers=from_transfers,
	         suggested_from_transfers=suggested_from_transfers,
	         suggested_to_transfers=suggested_to_transfers)
	c.update(csrf(request))
	return render_to_response("crep/index.html", c)


@login_required
def add_transfer(request):
	user = get_user_profile(request)
	to = UserProfile.objects.get(id=request.REQUEST["to"])
	unit = request.REQUEST.get("unit", "pence")
	ammount = {"pence":int, "pounds":money_parse}[unit](request.REQUEST["ammount"])
	
	transaction = Transaction(sender=user,
	                           recipient=to,
	                           sent=True,
	                           recieved=False,
	                           ammount=ammount)
	transaction.save()
	return return_to_previous(request)


@login_required
def cancel_transfer(request, id):
	user = get_user_profile(request)
	transfer = get_object_or_404(Transaction, id=int(id), sender=user)
	transfer.delete()
	return return_to_previous(request)


@login_required
def confirm_transfer(request, id):
	user = get_user_profile(request)
	transfer = get_object_or_404(Transaction, id=int(id), recipient=user)
	transfer.recieved = True
	transfer.save()
	return return_to_previous(request)


@login_required
def user(request, username):
	user = get_user_profile(request)
	return HttpResponse("User: %s" % len(user.transactions_sent.all()))


@login_required
def purchase(request, id):
	purchase = get_object_or_404(Purchase, id=id)
	return HttpResponse(repr(dir(purchase)))


@login_required
def purchase_add(request):
	users = UserProfile.objects.all()
	c = dict(users=users)
	c.update(csrf(request))
	return render_to_response("crep/add_purchase.html", c)


@login_required
def purchase_add_submit(request):
	purchase = Purchase(title=request.REQUEST.get("title", ""),
	                    description=request.REQUEST.get("description", ""),
	                    purchaser=UserProfile.objects.get(id=int(request.POST["purchaser"])))
	purchase.save()
	for user in UserProfile.objects.all():
		ammount = money_parse(request.REQUEST["w_%s_t" % user.id])
		ao = AmmountOwed(user=user, purchase=purchase, ammount=ammount)
		ao.save()
	return return_to_previous(request)


@login_required
def optimal_transfers(request):
	return render_to_response("crep/optimal_transfers.html",
	                          dict(transfers=TransactionCache.objects.all()))

@login_required
def email(request):
	vars = {}
	vars["from"] = time.localtime()
	vars["to"] = time.localtime()
	vars["transfers"] = TransactionCache.objects.all()
	return render_to_response("crep/email.html", vars)
