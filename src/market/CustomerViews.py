from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from market.forms import CustomerForm
from market.models import Customer, Stock, Category, Item
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class CustomerRegisterView(View):
    def get(self, request):
        return render(request, 'customer_register.html')

    def post(self, request):
        registered = False
        if request.method == 'POST':
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
                registered = True
            else:
                print(customer_form.errors)
        else:
            customer_form = CustomerForm()
        return render(request, 'customer_register.html', {'customer_form': customer_form,
                                                          'registered': registered})


class CustomerProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        print('get')
        user = request.user
        print(user, 1)
        customer = Customer.objects.get(user=user)
        print(customer, 2)
        context_dict = {}
        context_dict['customer'] = customer
        print(context_dict, 3)
        return render(request, 'customer_profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        print('post')
        username = request.user.username
        context_dict = {'username': username}
        return render(request, 'customer_profile.html', context_dict)


class CustomerStockListView(View):
    @method_decorator(login_required)
    def get(self, request):
        print(1)
        stocks = Stock.objects.all()
        print(stocks)
        context_dict = {}
        context_dict['stocks'] = stocks
        print(context_dict)
        return render(request, 'stock_list.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        print('post')
        return render(request, 'stock_list.html')


class CustomerStockCategoryListView(View):
    @method_decorator(login_required)
    def get(self, request, id):
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

    @method_decorator(login_required)
    def post(self, request, id):
        print('post')
        return render(request, 'category_list.html', {'id': id})


class CustomerStockCategoryItemListView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        print('get')
        category = Category.objects.get(id=id)
        print(category, 1)
        items = Item.objects.filter(category=category)
        print(items, 2)
        context_dict = {}
        context_dict['category'] = category
        context_dict['items'] = items
        return render(request, 'item_list.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        print('post')
        return render(request, 'item_list.html', {'id': id})
