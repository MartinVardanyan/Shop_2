from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from market.forms import AdminForm, StockForm, CategoryForm, ItemForm
from market.models import Administrator, Stock, Item, Category, MyBug
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse


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
            admin = Administrator.objects.get(user=user)
            print(admin.avatar, 2)
            print(admin)
            avatar = admin.avatar
            stock = Stock.objects.get(admin=admin)
            print(stock)
            print(stock.name)
            stockname = stock.name
            stock_id = stock.id
            print(2.5)
            context_dict = {'username': user,
                            'stockname': stockname,
                            'avatar': avatar,
                            'id': stock_id}
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
            admin = Administrator.objects.get(user=user)
            print(2)
            stock = Stock.objects.get(admin=admin)
            stockname = stock.name
            print(stock, stockname, 4)
            if Category:
                print(5)
                context_dict = {}
                category = Category.objects.filter(stock=stock)
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
                admin = Administrator.objects.get(user=user)
                print(admin, 5)
                stock = Stock.objects.get(admin=admin)
                shop = stock
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


class AdminEditStockNameView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        stock = Stock.objects.get(id=id)
        context_dict = {}
        context_dict['stock'] = stock.id
        return render(request,'edit_stock_name.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            #user = request.user
            #admin = Administrator.objects.get(user=user)
            stock = Stock.objects.get(id=id)
            #avatar = admin.avatar
            print(1, stock)
            edit = False
            if request.method == 'POST':
                print(2)
                stock.name = request.POST.get('name')
                print(stock.name, 3)
                stock.save()
                print(4)
                edit = True
                #context_dict = {}
                #context_dict['id'] = stock.id
                #context_dict['stockname'] = stock.name
                #context_dict['username'] = user
                #context_dict['avatar'] = avatar
                return render(request, 'edit_stock_name.html', {'edit': edit})#, context_dict)
            else:
                return render(request, "edit_stock_name.html", {"stock": stock,
                                                                'edit': edit})
        except Stock.DoesNotExist:
            return HttpResponse("<h2>Stock not found</h2>")


class AdminEditCategoryNameView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        category = Category.objects.get(id=id)
        context_dict = {}
        context_dict['stock'] = category.id
        return render(request, 'edit_category_name.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            #user = request.user
            print(1)
            #admin = Administrator.objects.get(user=user)
            print(2)
            #stock = Stock.objects.get(admin=admin)
            #stockname = stock.name
            categories = Category.objects.get(id=id)
            #category = Category.objects.filter(stock=stock)
            print(1.5)
            edit = False
            if request.method == 'POST':
                print(2)
                categories.name = request.POST.get('name')
                print(categories.name, 3)
                categories.save()
                print(4)
                edit = True
                #context_dict = {}
                #context_dict['categories'] = category
                #context_dict['stock_name'] = stockname
                return render(request, 'edit_category_name.html', {'edit': edit})
            else:
                return render(request, "edit_category_name.html", {"category": categories,
                                                                   'edit': edit})
        except Category.DoesNotExist:
            return HttpResponse("<h2>Category not found</h2>")


class AdminEditItemNameView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        item = Item.objects.get(id=id)
        context_dict = {}
        context_dict['stock'] = item.id
        return render(request, 'edit_item_name.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            #user = request.user
            #admin = Administrator.objects.get(user=user)
            #stock = Stock.objects.get(admin=admin)
            item = Item.objects.get(id=id)
            #category = item.category
            #items = Item.objects.filter(category=category, stock=stock)
            #print(category, 2)
            edit = False
            if request.method == 'POST':
                item.name = request.POST.get('name')
                print(item.name, 3)
                item.save()
                print(4)
                #context_dict = {}
                #print(5)
                #context_dict['item'] = items
                #context_dict['category'] = category
                #print(context_dict)
                edit = True
                return render(request, 'edit_item_name.html', {'edit': edit})
            else:
                return render(request, "edit_item_name.html", {"item": item,
                                                               'edit': edit})
        except Item.DoesNotExist:
            return HttpResponse("<h2>Item not found</h2>")


class AdminEditItemPriceView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        item = Item.objects.get(id=id)
        context_dict = {}
        context_dict['stock'] = item.id
        return render(request, 'edit_item_price.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            #user = request.user
            #admin = Administrator.objects.get(user=user)
            #stock = Stock.objects.get(admin=admin)
            item = Item.objects.get(id=id)
            #category = item.category
            #items = Item.objects.filter(category=category, stock=stock)
            #print(category, 2)
            edit = False
            if request.method == 'POST':
                item.price = request.POST.get('price')
                print(item.price, 3)
                item.save()
                edit = True
                print(4)
                #context_dict = {}
                print(5)
                #context_dict['item'] = items
                #context_dict['category'] = category
                #print(context_dict)
                return render(request, 'edit_item_price.html', {'edit': edit})
            else:
                return render(request, "edit_item_price.html", {"item": item,
                                                                'edit': edit})
        except Item.DoesNotExist:
            return HttpResponse("<h2>Item not found</h2>")


class AdminEditItemQuanityView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        item = Item.objects.get(id=id)
        context_dict = {}
        context_dict['stock'] = item.id
        return render(request, 'edit_item_quanity.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            #user = request.user
            #admin = Administrator.objects.get(user=user)
            #stock = Stock.objects.get(admin=admin)
            item = Item.objects.get(id=id)
            #category = item.category
            #items = Item.objects.filter(category=category, stock=stock)
            #print(category, 2)
            edit= False
            if request.method == 'POST':
                item.quanity = request.POST.get('quanity')
                print(item.quanity, 3)
                item.save()
                print(4)
                #context_dict = {}
                print(5)
                #context_dict['item'] = items
                #context_dict['category'] = category
                #print(context_dict)
                edit =True
                return render(request, 'edit_item_quanity.html', {'edit': edit})
            else:
                return render(request, "edit_item_quanity.html", {"item": item,
                                                                  'edit': edit})
        except Item.DoesNotExist:
            return HttpResponse("<h2>Item not found</h2>")


class AdminIncomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        income = False
        if request.method == 'GET':
            print(1)
            user = request.user
            print(user, 2)
            admin = Administrator.objects.get(user=user)
            print(admin, 3)
            stock = Stock.objects.get(admin=admin)
            print(stock, 4)
            item = Item.objects.filter(stock=stock)
            print(item, 5)
            buy_items = MyBug.objects.filter(item=item[0])
            print(buy_items, 6)
            context_dict = {}
            print(income)
            for i in buy_items:
                print(6.5)
                x = int(i.item.price) * int(i.item.quanity)
                print(x, 7)
                context_dict['income'] = x
                context_dict['sold_items'] = i
                print(context_dict, 8)
                income = True
                print(income)
            context_dict['income'] = income
            return render(request, 'income.html', context_dict)
        else:
            return render(request, 'income.html', {'income': income})

    @method_decorator(login_required)
    def post(self, request):
        print('post')
        return render(request, 'income.html')
