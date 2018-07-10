from django.contrib import admin

# Register your models here.

from django.contrib import admin
from emailautoverify.models import eMail
from emailautoverify.VerifyEmail import Verify_Emai
# from templates import automail
# Register your models here.

def AutoVerify(self,request,queryset):
    print(queryset)
    for i in queryset:
        emailaddr = i.email
        emailpsd = i.password
        print(emailaddr,emailpsd)
        Verify_Emai(emailaddr,emailpsd)

# class reFresh():
#     pass

def Addmore():
    pass

class emailAdmin(admin.ModelAdmin):
    list_display = ['email']
    actions = [AutoVerify]
    search_fields = ['email']
    # ordering =


admin.site.register(eMail, emailAdmin)