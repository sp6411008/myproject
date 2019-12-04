from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	address=models.TextField(null=True)
	mobile=models.CharField(max_length=100)
	birth_date=models.DateTimeField(null=True,blank=True)
	password=models.CharField(max_length=100)
	confirm_password=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="inactive")
	user_image=models.ImageField(upload_to='images/',blank=True,null=True)


	def __str__(self):
		return self.first_name+" "+self.last_name
class Products(models.Model):
	CHOICES = (
        ("Fashion",'Fashion'),
        ("Electronics",'Electronics'),
        ("Home Appliance",'Home Appliance'),
    )
	product_category=models.CharField(max_length=50,choices=CHOICES,default="")
	product_name=models.CharField(max_length=50)
	product_brand=models.CharField(max_length=50)
	product_image=models.ImageField(upload_to='images/')
	product_price=models.IntegerField(default=0)
	product_desc=models.TextField()
	product_sale=models.BooleanField(default=False)
	product_sale_percentage=models.IntegerField(default=0)
	after_dicount_price=models.IntegerField(default=0)

	def __str__(self):
		return self.product_name
class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Products,on_delete=models.CASCADE)
	cart_date=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user.first_name
