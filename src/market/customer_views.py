# django imports
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# 3-th part imports
from market.forms import CustomerForm
from market.models import Customer, Stock, Category, Item, MyBag, Administrator


#
class CustomerRegisterView(View):
    def get(self, request):
        customer = CustomerForm(data=request.GET)
        is_register = True
        return render(request, 'customer_register.html', {'customer': customer, 'is_register': is_register})

    def post(self, request):
        customer_form = CustomerForm(data=request.POST)

        if customer_form.is_valid():
            data = customer_form.cleaned_data
            user = User.objects.create_user(data['username'],
                                            data['email'],
                                            data['password'])
            user.is_active = True
            user.save()
            customer = Customer.objects.create(user=user, avatar=request.FILES['avatar'])
            customer.save()
            return render(request, 'login.html')
        else:
            return render(request, 'customer_register.html')


#
class CustomerProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            my_bag = MyBag.objects.filter(customer=customer)
            context_dict = {}
            context_dict['customer'] = customer
            context_dict['my_bag'] = my_bag
            return render(request, 'customer_profile.html', context_dict)
        except Customer.DoesNotExist:
            return HttpResponse("We can't find this customer!")


#
class CustomerGetView(View):
    @staticmethod
    @login_required
    def get_stock_list(request):
        stocks = Stock.objects.all()
        context_dict = {}
        context_dict['stocks'] = stocks
        return render(request, 'stock_list.html', context_dict)

    @staticmethod
    @login_required
    def get_category_list(request, id):
        try:
            stock = Stock.objects.get(id=id)
            admin = stock.admin
            categories = Category.objects.filter(stock=stock)
            context_dict = {}
            context_dict['categories'] = categories
            context_dict['stock'] = stock
            context_dict['admin'] = admin
            return render(request, 'category_list.html', context_dict)
        except Stock.DoesNotExist:
            return HttpResponse("<h2>We can't find this stock!</h2>")

    @staticmethod
    @login_required
    def get_item_list(request, id):
        try:
            category = Category.objects.get(id=id)
            stock = category.stock
            admin = stock.admin
            items = Item.objects.filter(category=category, admin=admin)
            context_dict = {}
            context_dict['category'] = category
            context_dict['items'] = items
            return render(request, 'item_list.html', context_dict)
        except Category.DoesNotExist:
            return HttpResponse("<h2>We can't find this category!</h2>")


#
class CustomerMyBagView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            my_bag = MyBag.objects.filter(customer=customer)
            context_dict = {}
            context_dict['customer'] = customer
            context_dict['items'] = my_bag
            return render(request, 'my_bag.html', context_dict)
        except MyBag.DoesNotExist:
            return HttpResponse("<h2>We can't find your bug</h2>")

    @staticmethod
    def check_view(request, id):
        if request.method == "POST":
            return CustomerMyBagView.create_my_bag(request, id)
        elif request.method == 'GET':
            return CustomerMyBagView.get_list(request, id)

    @staticmethod
    @login_required
    def get_list(request, id):
        return render(request, 'add_item_my_bag.html', {'id': id})

    @staticmethod
    @login_required
    def create_my_bag(request, id):
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            x = request.POST.get('quanity')
            item = Item.objects.get(id=id)
            category = item.category
            stock =category.stock

            if float(x) > float(item.quanity) or float(x) <= 0:
                errors = {'message': "We don't have so many quanity!"}
                return render(request, 'add_item_my_bag.html', {'error': errors})
            else:
                item.quanity = item.quanity - float(request.POST.get('quanity'))
                item.save()
                my_bag_item = Item()
                my_bag_item.stock = item.stock
                my_bag_item.category = item.category
                my_bag_item.name = item.name
                my_bag_item.price = item.price
                my_bag_item.picture = item.picture
                my_bag_item.customer = customer
                my_bag_item.info = item.info
                my_bag_item.quanity = request.POST.get('quanity')
                my_bag_item.save()
                my_bag = MyBag()
                my_bag.customer = customer
                my_bag.item = my_bag_item
                my_bag.save()
                return redirect(reverse('market:category_list', args=[stock.id]))
        except Item.DoesNotExist:
            return render(request, 'add_item_my_bag.html.html', {'id': id})

    @staticmethod
    @login_required
    def remove(request, id):
        is_remove = False
        try:
            item = Item.objects.get(id=id)
            item.delete()
            is_remove = True
            return render(request, 'remove_item_my_bag.html', {'is_remove': is_remove})
        except Item.DoesNotExist:
            return render(request, 'remove_item_my_bag.html', {'is_remove': is_remove})
