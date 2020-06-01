# django imports
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

# 3-th part imports
from market.forms import CustomerForm
from market.models import Customer, Stock, Category, Item, MyBug, Administrator


#
class Customer_Register_View(View):
    def get(self, request):
        customer = CustomerForm(data=request.GET)
        return render(request, 'customer_register.html', {'customer': customer})

    def post(self, request):
        customer_form = CustomerForm(data=request.POST)

        if customer_form.is_valid():
            data = customer_form.cleaned_data

            if data['password'] != data['password2']:
                print('Not separate password!')
                return render(request, 'customer_register.html', {'customer': customer_form})
            else:
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
class Customer_Profile_View(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            print('get')
            user = request.user
            print(user, 1)
            customer = Customer.objects.get(user=user)
            my_bug = MyBug.objects.filter(customer=customer)
            print(customer, 2)
            context_dict = {}
            context_dict['customer'] = customer
            context_dict['my_bug'] = my_bug
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
class CustomerMyBugView(View):
    @method_decorator(login_required)
    def get(self, request):
        print(0)
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            print(1)
            my_bug = MyBug.objects.filter(customer=customer)
            print(2, my_bug)
            context_dict = {}
            context_dict['customer'] = customer
            print(context_dict, 3)
            context_dict['items'] = my_bug
            print(context_dict, 4)
            return render(request, 'my_bug.html', context_dict)
        except MyBug.DoesNotExist:
            return HttpResponse("<h2>We can't find your bug</h2>")

    @staticmethod
    def check_view(request, id):
        if request.method == "POST":
            print('post')
            return CustomerMyBugView.create_obj(request, id)
        elif request.method == 'GET':
            print('get')
            return CustomerMyBugView.get_list(request, id)

    @staticmethod
    @login_required
    def get_list(request, id):
        return render(request, 'add_item_my_bug.html', {'id': id})

    @staticmethod
    @login_required
    def post(request, id):
        is_add = False
        try:
            print(1)
            user = request.user
            customer = Customer.objects.get(user=user)
            x = request.POST.get('quanity')
            item = Item.objects.get(id=id)

            if int(x) > int(item.quanity):
                print('error')
                erors = {'message': 'We dont have so many quanity!'}
                return render(request, 'add_item_my_bug.html', {'error': erors})
            else:
                item.quanity = item.quanity - int(request.POST.get('quanity'))
                item.save()
                print(2, item)
                my_bug_item = Item()
                my_bug_item.stock = item.stock
                my_bug_item.category = item.category
                my_bug_item.name = item.name
                my_bug_item.price = item.price
                my_bug_item.picture = item.picture
                my_bug_item.customer = customer
                my_bug_item.quanity = request.POST.get('quanity')
                my_bug_item.save()

                # my_bug_item = item
                # my_bug_item.customer = customer
                # my_bug_item.quanity = request.POST.get('quanity')
                # my_bug_item.admin = None
                # my_bug_item.save()
                print(my_bug_item)
                my_bug = MyBug()
                my_bug.customer = customer
                my_bug.item = my_bug_item
                print(my_bug.item)
                my_bug.save()
                print(3, my_bug)
                is_add = True
                return render(request, 'add_item_my_bug.html', {'is_add': is_add,
                                                                'item': my_bug_item})
        except Item.DoesNotExist:
            return render(request, 'add_item_my_bug.html.html', {'is_add': is_add,
                                                                 'id': id})

    @staticmethod
    @login_required
    def remove(request, id):
        is_remove = False
        try:
            item = Item.objects.get(id=id)
            item.delete()
            is_remove = True
            return render(request, 'remove_item_my_bug.html', {'is_remove': is_remove})
        except Item.DoesNotExist:
            return render(request, 'remove_item_my_bug.html', {'is_remove': is_remove})
