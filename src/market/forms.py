# django imports
from django import forms

# 3-th part imports
from market.models import Administrator, Stock, User, Customer, Category, Item


#
class AdminForm(forms.ModelForm):
    username = forms.CharField(max_length=100, help_text="Please enter your name.")
    email = forms.EmailField(max_length=100, help_text="Please enter your email address.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter your password.")
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text="Please repeat your password. ")

    #
    class Meta:
        model = Administrator
        fields = ('username', 'email', 'password', 'password2', 'avatar')


#
class StockForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Please add your stock dear Administrator.")

    #
    class Meta:
        model = Stock
        fields = ('name',)


#
class CustomerForm(forms.ModelForm):
    username = forms.CharField(max_length=100, help_text="Please enter your name.")
    email = forms.EmailField(max_length=100, help_text="Please enter your email address.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter your password.")
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text="Please repeat your password.")

    #
    class Meta:
        model = Customer
        fields = ('username', 'email', 'password', 'password2', 'avatar')


#
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Please enter the category name.")

    #
    class Meta:
        model = Category
        fields = ('name',)


#
class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Please enter the item name.')
    price = forms.IntegerField(help_text='Please enter the price of item.')
    quanity = forms.IntegerField(help_text="Please enter the quanity of item.")

    #
    class Meta:
        model = Item
        fields = ('name', 'price', 'quanity', 'picture')
