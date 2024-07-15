from django.contrib import admin
from .models import *
'''
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name','img','description')
    admin.site.register(catagory,CatagoryAdmin)
'''
admin.site.register(catagory)
admin.site.register(Product)

