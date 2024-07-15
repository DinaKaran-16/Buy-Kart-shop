from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time,filename)
    return os.path.join('upload/',new_filename)



class catagory(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    img = models.ImageField(upload_to=getFileName,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-hidden")
    
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name
    


class Product(models.Model):
    catagory=models.ForeignKey(catagory,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    vendor = models.CharField(max_length=150,null=False,blank=False)
    product_img = models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    orginal_price = models.FloatField(null=False,blank=False)
    offer_price = models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-hidden")
    trending = models.BooleanField(default=False,help_text="0-default,1-trending")
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qyt=models.IntegerField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)

    