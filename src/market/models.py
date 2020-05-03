from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrated_at = models.DateTimeField(default=datetime.now)
    avatar = models.ImageField(upload_to='admin_profile_avatar', blank=True)

    def __repr__(self):
        return self.user.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrated_at = models.DateTimeField(default=datetime.now)
    avatar = models.ImageField(upload_to='customer_profile_avatar', blank=True)

    def __repr(self):
        return self.user.username


class Stock(models.Model):
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __repr__(self):
        return "{} {}".format(self.admin, self.name)


class Category(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __repr__(self):
        return self.name


class Item(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    price = models.IntegerField(default=0)
    quanity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='item_pictures', blank=True)
    is_removed = models.BooleanField(default=False)

    def __repr__(self):
        return "{} {} {} {} {}".format(self.stock, self.category, self.name, self.price, self.quanity)


class MyBug(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buy_time = models.DateTimeField(default=datetime.now)

    def __repr__(self):
        return "{} {} {}".format(self.customer, self.item, self.buy_time)
