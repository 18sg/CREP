from mt.crep.models import *
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
	readonly_fields = ("ammount_owed_current",)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register([Transaction, Purchase, AmmountOwed])
