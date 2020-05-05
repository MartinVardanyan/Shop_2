from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from market.forms import AdminForm, StockForm, CategoryForm, ItemForm
from market.models import Administrator, Stock, Item, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class AdminRegisterView(View):
    def get(self, request):
        return render(request, 'admin_register.html')

    def post(self, request):
        registered = False
        print(1)
        if request.method == 'POST':
            print(2)
            admin_form = AdminForm(data=request.POST)
            print(3)
            stock_form = StockForm(data=request.POST)
            if admin_form.is_valid() and stock_form.is_valid():
                data = admin_form.cleaned_data
                print(data, 4)
                user = User.objects.create_user(data['username'],
                                                data['email'],
                                                data['password'])
                print(5)
                #user.first_name = data['first_name']
                #user.last_name = data['last_name']
                user.is_active = True
                user.save()
                print(user, 6)
                admin = Administrator.objects.create(user=user, avatar=request.FILES['avatar'])
                print(7)
                admin.save()
                print(8)
                stock = Stock.objects.create(admin=admin, name=request.POST['name'])
                print(9)
                stock.save()
                print(10)
                print(11)
                registered = True
            else:
                print(admin_form.errors, stock_form.errors)
        else:
            admin_form = AdminForm()
            stock_form = StockForm()
        return render(request, 'admin_register.html', {'admin_form': admin_form,
                                                       'stock_form': stock_form,
                                                       'registered': registered})


class AdminProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.method == 'GET':
            print(0)
            user = request.user
            print(user, 1)
            admin = Administrator.objects.filter(user=user)
            print(admin[0].avatar, 13)
            print(admin)
            avatar = admin[0].avatar
            stock = Stock.objects.filter(admin=admin[0])
            print(stock[0])
            print(stock[0].name)
            stockname = stock[0].name
            print(2.5)
            context_dict = {'username': user,
                            'stockname': stockname,
                            'avatar': avatar}
            print(context_dict, 3)
            return render(request, 'admin_profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        print(5)
        username = request.user.username
        context_dict = {'username': username}
        return render(request, 'admin_profile.html', context_dict)


class AdminStockView(View):
    @method_decorator(login_required)
    def get(self, request):
        #global context_list
        if request.method == 'GET':
            print(0)
            user = request.user
            print(1)
            admin = Administrator.objects.filter(user=user)
            print(2)
            stock = Stock.objects.filter(admin=admin[0])
            stockname = stock[0].name
            print(stock, stockname, 4)
            if Category:
                print(5)
                context_dict = {}
                category = Category.objects.filter(stock=stock[0])
                context_dict['categories'] = category
                context_dict['stock_name'] = stockname
                print(context_dict)
                return render(request, 'my_stock.html', context_dict)

            else:
                category = print("You dont have category in your stock!")
                context_dict = {'stock': stockname,
                                'category': category}
                return render(request, 'my_stock.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        return render(request, 'my_stock.html')


class AdminCategoryView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        if request.method == 'GET':
            category = Category.objects.get(id=id)
            print(category, 3)
            if Item:
                print(4)
                context_dict = {}
                item = Item.objects.filter(category=category)
                context_dict['item'] = item
                context_dict['category'] = category
                print(context_dict)
                return render(request, 'category.html', context_dict)
            else:
                item = print("Your category dont have item, please add!")
                context_dict = {'item': item}
                print(context_dict)
                return render(request, 'category.html', context_dict)

    @method_decorator(login_required)
    def post(self, request):
        return render(request, 'category.html')


class AdminAddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'add_category.html')

    @method_decorator(login_required)
    def post(self, request):
        addcategory = False
        if request.method == 'POST':
            print(0)
            category_form = CategoryForm(data=request.POST)
            print(1)
            if category_form.is_valid():
                print(2)
                data = category_form.cleaned_data
                print(data, 3)
                user = request.user
                print(user, 4)
                admin = Administrator.objects.filter(user=user)
                print(admin, 5)
                stock = Stock.objects.filter(admin=admin[0])
                shop = stock[0]
                print(stock, 6)
                category = Category.objects.create(stock=shop, name=request.POST['name'])
                print(category, 7)
                category.save()
                print(8)
                addcategory = True
            else:
                print(category_form.errors)
        else:
            category_form = CategoryForm()
        return render(request, 'add_category.html', {'category_form': category_form,
                                                     'addcategory': addcategory})


class AdminAddItemView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        context_dict = {}
        context_dict['category'] = category
        print(context_dict, 0)
        return render(request, 'add_item.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        print(category, 1)
        additem = False
        if request.method == 'POST':
            print(2)
            item_form = ItemForm(data=request.POST)
            if item_form.is_valid():
                data = item_form.cleaned_data
                print(data, 3)
                user = request.user
                print(user, 4)
                admin = Administrator.objects.get(user=user)
                print(admin, 5)
                stock = Stock.objects.get(admin=admin)
                print(stock, 6)
                category = Category.objects.get(id=id)
                print(category, 7)
                item = Item.objects.create(stock=stock, category=category, name=request.POST['name'], price=request.POST['price'], quanity=request.POST['quanity'], picture=request.FILES['picture'])
                item.save()
                print(item, 8)
                additem = True
            else:
                print(item_form.errors)
        else:
            item_form = ItemForm()
        return render(request, 'add_item.html', {'item_form': item_form,
                                                 'additem': additem,
                                                 'category': category})
