from django.http import HttpResponse
from mt.crep.models import *
from django.shortcuts import render_to_response, get_object_or_404

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
	return render_to_response("crep/add_purchase.html", dict(users=users))
