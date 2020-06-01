# django imports
from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse

# 3-th part imports
from market.forms import AdminForm, StockForm, CategoryForm, ItemForm
from market.models import Administrator, Stock, Item, Category, MyBug, Customer


#
class AdminRegisterView(View):
    def get(self, request):
        admin_form = AdminForm(data=request.GET)
        print(3)
        stock_form = StockForm(data=request.GET)
        return render(request, 'admin_register.html', {'admin': admin_form, 'stock': stock_form})

    def post(self, request):
        print(1)
        print(2)
        admin_form = AdminForm(data=request.POST)
        print(3)
        stock_form = StockForm(data=request.POST)

        if admin_form.is_valid() and stock_form.is_valid():
            print(3.5)
            data = admin_form.cleaned_data

            if data['password'] != data['password2']:
                print('Not separate password!')
                return render(request, 'admin_register.html', {'admin': admin_form,
                                                               'stock': stock_form})
            else:
                print(data, 4)
                user = User.objects.create_user(data['username'],
                                                data['email'],
                                                data['password'])
                print(5)
                user.is_active = True
                user.save()
                print(user.password, 6)
                admin = Administrator.objects.create(user=user, avatar=request.FILES['avatar'])
                print(admin)
                print(7)
                admin.save()
                print(8)
                stock = Stock.objects.create(admin=admin, name=request.POST['name'])
                print(9)
                stock.save()
                print(10)
                return render(request, 'login.html')
        else:
            print(admin_form.errors, stock_form.errors)
            return render(request, 'admin_register.html')


#
class AdminProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        print(0)
        user = request.user
        print(user, 1)

        try:
            admin = Administrator.objects.get(user=user)
            print(admin.avatar, 2)
            print(admin)
            avatar = admin.avatar
            stock = Stock.objects.get(admin=admin)
            print(stock)
            print(stock.name)
            stock_name = stock.name
            stock_id = stock.id
            print(2.5)
            context_dict = {'username': user,
                            'stockname': stock_name,
                            'avatar': avatar,
                            'id': stock_id}
            print(context_dict, 3)
            return render(request, 'admin_profile.html', context_dict)

        except Administrator.DoesNotExist:
            print("<h2>We can't find this admin!</h2>")


#
class AdminStockView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        return render(request, 'edit_stock_name.html', {'id': id})

    @method_decorator(login_required)
    def post(self, request, id):
        is_edit = False
        try:
            stock = Stock.objects.get(id=id)
            print(1, stock)
            print(2)
            stock.name = request.POST.get('name')
            print(stock.name, 3)
            stock.save()
            print(4)
            is_edit = True
            return render(request, 'edit_stock_name.html', {'is_edit': is_edit})

        except Stock.DoesNotExist:
            return render(request, 'edit_stock_name.html', {'is_edit': is_edit})

    @staticmethod
    def check_view(request):
        print('check_view')
        if request.method == 'GET':
            print('get')
            return AdminStockView.get_list(request)
        else:
            return HttpResponse('<h2>Method not allowed!</h2>')

    @staticmethod
    @login_required
    def get_list(request):
        print(0)
        user = request.user
        print(1)

        try:
            admin = Administrator.objects.get(user=user)
            print(2)
            stock = Stock.objects.get(admin=admin)
            stock_name = stock.name
            print(stock, stock_name, 4)

            if len(Category.objects.filter(stock=stock)) > 0:
                print(5)
                context_dict = {}
                category = Category.objects.filter(stock=stock)
                context_dict['categories'] = category
                context_dict['stock_name'] = stock_name
                print(context_dict)
                return render(request, 'my_stock.html', context_dict)

            else:
                category = "You don't have category in your stock!"
                context_dict = {'stock': stock_name,
                                'category': category}
                return render(request, 'my_stock.html', context_dict)

        except Administrator.DoesNotExist:
            print("<h2>We can't find this stock!</h2>")


#
class AdminCategoryView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            user = request.user
            admin = Administrator.objects.get(user=user)
            print(category, 3)

            if len(Item.objects.filter(category=category)):
                print(4)
                context_dict = {}
                item = Item.objects.filter(category=category, admin=admin)
                print(5)
                context_dict['item'] = item
                context_dict['category'] = category
                print(context_dict)
                return render(request, 'category.html', context_dict)

            else:
                return render(request, 'category.html')

        except Category.DoesNotExist:
            return HttpResponse("<h2>We can't find this category</h2>")

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            print(1)
            category = Category.objects.get(id=id)
            print(2)
            name = request.POST.get('name', None)

            if name:
                category.name = request.POST.get('name')
                print(category.name, 3)
                category.save()
            print(4)
            is_edit = True
            return render(request, 'edit_category_name.html', {'is_edit': is_edit,
                                                               'category': category})

        except Category.DoesNotExist:
            return HttpResponse("<h2>Category not found</h2>")

    @staticmethod
    def check_view(request):
        print('check_view')
        if request.method == 'GET':
            print('get')
            return AdminCategoryView.get_category_page(request)
        elif request.method == "POST":
            print('post')
            return AdminCategoryView.edit_category(request)
        else:
            return HttpResponse('Method not allowed!')

    @staticmethod
    @login_required
    def patch(request):
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

                try:
                    admin = Administrator.objects.get(user=user)
                    print(admin, 5)
                    stock = Stock.objects.get(admin=admin)
                    shop = stock
                    print(stock, 6)
                    category = Category.objects.create(stock=shop, name=request.POST['name'])
                    print(category, 7)
                    category.save()
                    print(8)
                    is_add_category = True
                    return render(request, 'add_category.html', {'is_add_category': is_add_category})

                except Administrator.DoesNotExist:
                    print("We can't find this admin!")
            else:
                print(category_form.errors)
        else:
            is_add_category = False
            category_form = CategoryForm()
            return render(request, 'add_category.html', {'category_form': category_form,
                                                         'is_add_category': is_add_category})


#
class AdminItemView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        is_add_item = False
        item_form = ItemForm(data=request.GET)
        return render(request, 'add_item.html', {'category': category,
                                                 'is_add_item': is_add_item,
                                                 "item_form": item_form})

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        print(category, 1)
        is_add_item = False
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
            item = Item.objects.create(stock=stock, category=category, admin=admin,
                                       name=request.POST['name'], price=request.POST['price'],
                                       quanity=request.POST['quanity'],
                                       picture=request.FILES['picture'])
            item.save()
            print(item, 8)
            is_add_item = True
            return render(request, 'add_item.html', {'is_add_item': is_add_item,
                                                     'category': category})
        else:
            print(item_form.errors)
            return render(request, 'add_item.html', {'item_form': item_form,
                                                     'is_add_item': is_add_item,
                                                     'category': category})

    @staticmethod
    def check_view(request, id):
        print('check_view')
        if request.method == 'POST':
            print('post')
            return AdminItemView.patch(request, id)
        elif request.method == 'GET':
            print('get')
            return AdminItemView.patch(request, id)
        else:
            return HttpResponse('Method not allowed!')

    @staticmethod
    @login_required
    def patch(request, id):
        is_edit = False
        if request.method == 'POST':
            try:
                item = Item.objects.get(id=id)
                name = request.POST.get('name', None)
                price = request.POST.get('price', None)
                quanity = request.POST.get('quanity', None)
                if price:
                    item.price = price
                if name:
                    item.name = name
                if quanity:
                    item.quanity = quanity
                item.save()
                print(4)
                is_edit = True
                return render(request, 'edit_item.html', {'is_edit': is_edit, 'item': item})
            except Item.DoesNotExist:
                return HttpResponse("We don't find this item")
        else:
            return render(request, 'edit_item.html', {'is_edit': is_edit})


#
class Admin_Income_View(View):  # class name 
    @method_decorator(login_required)
    def get(self, request):
        is_income = False
        try:
            print(1)
            user = request.user
            print(user, 2)
            admin = Administrator.objects.get(user=user)
            print(admin, 3)
            stock = Stock.objects.get(admin=admin)
            print(stock, 4)
            items = Item.objects.filter(stock=stock, admin__isnull=True)
            print(items, 5)
            context_dict = {}
            if items:
                print(items)
                context_dict['sold_items'] = items
                print(context_dict)
                print(6)
                x = 0
            for i in items:
                x += i.price * i.quanity
                print(x, 8)
                context_dict['income'] = x
            print(context_dict, 9)
            return render(request, 'income.html', context_dict)
        except Stock.DoesNotExist:
            return render(request, 'income.html', {'income': is_income})
