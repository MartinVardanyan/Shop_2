# django imports
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

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
            print(customer_form.errors)
        return render(request, 'customer_register.html')


#
class CustomerProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            print('get')
            user = request.user
            print(user, 1)
            customer = Customer.objects.get(user=user)
            my_bag = MyBag.objects.filter(customer=customer)
            print(customer, 2)
            context_dict = {}
            context_dict['customer'] = customer
            context_dict['my_bag'] = my_bag
            print(context_dict, 3)
            return render(request, 'customer_profile.html', context_dict)
        except Customer.DoesNotExist:
            return HttpResponse("We can't find this customer!")


#
class CustomerGetView(View):
    @staticmethod
    @login_required
    def get_stock_list(request):
        print(1)
        stocks = Stock.objects.all()
        print(stocks)
        context_dict = {}
        context_dict['stocks'] = stocks
        print(context_dict)
        return render(request, 'stock_list.html', context_dict)

    @staticmethod
    @login_required
    def get_category_list(request, id):
        try:
            print('get')
            stock = Stock.objects.get(id=id)
            print(stock, 1)
            categories = Category.objects.filter(stock=stock)
            print(categories, 2)
            context_dict = {}
            context_dict['categories'] = categories
            context_dict['stock'] = stock
            print(context_dict, 3)
            return render(request, 'category_list.html', context_dict)
        except Stock.DoesNotExist:
            return HttpResponse("<h2>We can't find this stock!</h2>")

    @staticmethod
    @login_required
    def get_item_list(request, id):
        try:
            print('get')
            category = Category.objects.get(id=id)
            print(category.name)
            stock = category.stock
            print(stock)
            admin = stock.admin
            print(category, 1)
            items = Item.objects.filter(category=category, admin=admin)
            print(items, 2)
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
        print(0)
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            print(1)
            my_bag = MyBag.objects.filter(customer=customer)
            print(2, my_bag)
            context_dict = {}
            context_dict['customer'] = customer
            print(context_dict, 3)
            context_dict['items'] = my_bag
            print(context_dict, 4)
            return render(request, 'my_bag.html', context_dict)
        except MyBag.DoesNotExist:
            return HttpResponse("<h2>We can't find your bug</h2>")

    @staticmethod
    def check_view(request, id):
        if request.method == "POST":
            print('post')
            return CustomerMyBagView.create_my_bag(request, id)
        elif request.method == 'GET':
            print('get')
            return CustomerMyBagView.get_list(request, id)

    @staticmethod
    @login_required
    def get_list(request, id):
        return render(request, 'add_item_my_bag.html', {'id': id})

    @staticmethod
    @login_required
    def create_my_bag(request, id):
        is_add = False
        try:
            print(1)
            user = request.user
            customer = Customer.objects.get(user=user)
            x = request.POST.get('quanity')
            item = Item.objects.get(id=id)

            if int(x) > int(item.quanity) or int(x) <= 0:
                print('error')
                errors = {'message': "We don't have so many quanity!"}
                return render(request, 'add_item_my_bag.html', {'error': errors})
            else:
                item.quanity = item.quanity - int(request.POST.get('quanity'))
                item.save()
                print(2, item)
                my_bag_item = Item()
                my_bag_item.stock = item.stock
                my_bag_item.category = item.category
                my_bag_item.name = item.name
                my_bag_item.price = item.price
                my_bag_item.picture = item.picture
                my_bag_item.customer = customer
                my_bag_item.quanity = request.POST.get('quanity')
                my_bag_item.save()
                print(my_bag_item)
                my_bag = MyBag()
                my_bag.customer = customer
                my_bag.item = my_bag_item
                print(my_bag.item)
                my_bag.save()
                print(3, my_bag)
                is_add = True
                return render(request, 'add_item_my_bag.html', {'is_add': is_add,
                                                                'item': my_bag_item})
        except Item.DoesNotExist:
            return render(request, 'add_item_my_bag.html.html', {'is_add': is_add,
                                                                 'id': id})

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
