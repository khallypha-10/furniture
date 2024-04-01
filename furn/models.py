from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(upload_to='blog')


class Contact(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products')
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} | {self.user.username} | quantity : {self.quantity}"

    def prod(self):
        prod = self.product.price * self.quantity 
        return prod

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(blank_label="Select Country")
    address = models.CharField(max_length=500)
    state = models.CharField(max_length=50)
    zip = models.IntegerField()
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=254)

 

    class Meta:
        verbose_name_plural = 'Addresses'
    
    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_number = models.CharField(max_length=50)
    orderItem = models.ManyToManyField("OrderItem")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Orders'

    def get_total(self):
        total = 0
        for order_item in self.orderItem.all():
            total += order_item.prod()
        return total

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    



   