# django imports
from django import forms

# 3-th part imports
from market.models import Administrator, Stock, User, Customer, Category, Item


#
class AdminForm(forms.ModelForm):
    username = forms.CharField(max_length=100, help_text="Please enter your name.")
    email = forms.EmailField(max_length=100, help_text="Please enter your email address.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter your password.")
    re_password = forms.CharField(widget=forms.PasswordInput(), help_text="Please repeat your password. ")

    def clean(self):
        print("Clean\n")
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        print(password)
        re_password = cleaned_data.get("re_password")
        print(re_password)
        if password != re_password:
            print("Clean password\n")
            raise forms.ValidationError(
                "Passwords should match."
            )
        return cleaned_data

    #
    class Meta:
        model = Administrator
        fields = ('username', 'email', 'password', 're_password', 'avatar')


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
    re_password = forms.CharField(widget=forms.PasswordInput(), help_text="Please repeat your password.")

    def clean(self):
        print("Clean\n")
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        print(password)
        re_password = cleaned_data.get("re_password")
        print(re_password)
        if password != re_password:
            print("Clean password\n")
            raise forms.ValidationError(
                "Passwords should match."
            )
        return cleaned_data

    #
    class Meta:
        model = Customer
        fields = ('username', 'email', 'password', 're_password', 'avatar')


#
class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text="Please enter the category name.")

    #
    class Meta:
        model = Category
        fields = ('name', 'picture')


#
class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=100, help_text='Please enter the item name.')
    price = forms.FloatField(help_text='Please enter the price of item.')
    quanity = forms.FloatField(help_text="Please enter the quanity of item.")

    #
    class Meta:
        model = Item
        fields = ('name', 'price', 'quanity', 'picture')
