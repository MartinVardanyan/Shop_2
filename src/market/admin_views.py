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
from market.forms import AdminForm, StockForm, CategoryForm, ItemForm
from market.models import Administrator, Stock, Item, Category


#
class AdminRegisterView(View):
    def get(self, request):
        admin_form = AdminForm(data=request.GET)
        stock_form = StockForm(data=request.GET)
        is_register = True
        return render(request, 'admin_register.html', {'admin': admin_form, 'stock': stock_form, 'is_register': is_register})

    def post(self, request):
        admin_form = AdminForm(data=request.POST)
        stock_form = StockForm(data=request.POST)

        if admin_form.is_valid() and stock_form.is_valid():
            data = admin_form.cleaned_data
            user = User.objects.create_user(data['username'],
                                            data['email'],
                                            data['password'])
            user.is_active = True
            user.save()
            admin = Administrator.objects.create(user=user, avatar=request.FILES['avatar'])
            admin.save()
            stock = Stock.objects.create(admin=admin, name=request.POST['name'])
            stock.save()
            return render(request, 'login.html')
        else:
            print(admin_form.errors, stock_form.errors)
            return render(request, 'admin_register.html')


#
class AdminProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user

        try:
            admin = Administrator.objects.get(user=user)
            avatar = admin.avatar
            stock = Stock.objects.get(admin=admin)
            stock_name = stock.name
            stock_id = stock.id
            context_dict = {'username': user,
                            'stockname': stock_name,
                            'avatar': avatar,
                            'id': stock_id}
            return render(request, 'admin_profile.html', context_dict)

        except Administrator.DoesNotExist:
            return redirect(reverse('market:login'))


#
class AdminStockView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        return render(request, 'edit_stock_name.html', {'id': id})

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            stock = Stock.objects.get(id=id)
            stock.name = request.POST.get('name')
            stock.save()
            return redirect(reverse('market:admin_profile'))

        except Stock.DoesNotExist:
            return redirect(reverse('market:admin_profile'))

    @staticmethod
    def check_view(request):
        if request.method == 'GET':
            return AdminStockView.get_list(request)
        else:
            return HttpResponse('<h2>Method not allowed!</h2>')

    @staticmethod
    @login_required
    def get_list(request):
        user = request.user

        try:
            admin = Administrator.objects.get(user=user)
            stock = Stock.objects.get(admin=admin)
            stock_name = stock.name

            if len(Category.objects.filter(stock=stock)) > 0:
                context_dict = {}
                category = Category.objects.filter(stock=stock)
                context_dict['categories'] = category
                context_dict['stock_name'] = stock_name
                AdminCategoryView.as_view()
                return render(request, 'my_stock.html', context_dict)

            else:
                category = "You don't have category in your stock!"
                context_dict = {'stock': stock_name,
                                'category': category}
                return render(request, 'my_stock.html', context_dict)

        except Administrator.DoesNotExist:
            return redirect(reverse('market:login'))


#
class AdminCategoryView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
            user = request.user
            admin = Administrator.objects.get(user=user)
            if len(Item.objects.filter(category=category)):
                context_dict = {}
                item = Item.objects.filter(category=category, admin=admin)
                context_dict['item'] = item
                context_dict['category'] = category
                return render(request, 'category.html', context_dict)

            else:
                return render(request, 'category.html', {'category': category})

        except Category.DoesNotExist:
            return HttpResponse("<h2>We can't find this category</h2>")

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            category = Category.objects.get(id=id)
            name = request.POST.get('name', None)

            if name:
                category.name = request.POST.get('name')
                category.save()
            return redirect(reverse('market:category', args=[category.id]))

        except Category.DoesNotExist:
            return HttpResponse("<h2>Category not found</h2>")

    @staticmethod
    def check_view(request):
        if request.method == 'GET':
            return AdminCategoryView.get_category_page(request)
        elif request.method == "POST":
            return AdminCategoryView.add_category(request)
        else:
            return redirect(reverse('market:my_stock'))

    @staticmethod
    @login_required
    def add_category(request):
        category_form = CategoryForm(data=request.POST)

        if category_form.is_valid():
            user = request.user

            try:
                admin = Administrator.objects.get(user=user)
                stock = Stock.objects.get(admin=admin)
                shop = stock
                category = Category.objects.create(stock=shop, picture=request.FILES['picture'], name=request.POST['name'])
                category.save()
                return redirect(reverse('market:my_stock'))

            except Administrator.DoesNotExist:
                return redirect(reverse('market:my_stock'))

    @staticmethod
    @login_required
    def get_category_page(request):
        category_form = CategoryForm()
        return render(request, 'add_category.html', {'category_form': category_form})


#
class AdminItemView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        item_form = ItemForm(data=request.GET)
        return render(request, 'add_item.html', {'category': category,
                                                 "item_form": item_form})

    @method_decorator(login_required)
    def post(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            category = None
        item_form = ItemForm(data=request.POST)

        if item_form.is_valid():
            user = request.user
            admin = Administrator.objects.get(user=user)
            stock = Stock.objects.get(admin=admin)
            category = Category.objects.get(id=id)
            item = Item.objects.create(stock=stock, category=category, admin=admin,
                                       name=request.POST['name'], price=request.POST['price'],
                                       quanity=request.POST['quanity'],
                                       picture=request.FILES['picture'],
                                       info=request.POST['info'],)
            item.save()
            return redirect(reverse('market:category', args=[category.id]))

        else:
            return render(request, 'add_item.html', {'item_form': item_form,
                                                     'category': category})

    @staticmethod
    def check_view(request, id):
        if request.method == 'POST':
            return AdminItemView.edit_item(request, id)
        elif request.method == 'GET':
            return AdminItemView.get_edit_item(request, id)
        else:
            return HttpResponse('Method not allowed!')

    @staticmethod
    @login_required
    def edit_item(request, id):
        try:
            item = Item.objects.get(id=id)
            category = item.category
            name = request.POST.get('name', None)
            price = request.POST.get('price', None)
            quanity = request.POST.get('quanity', None)
            info = request.POST.get('info', None)
            if price:
                item.price = price
                item.save()
            if name:
                item.name = name
                item.save()
            if quanity:
                item.quanity = quanity
                item.save()
            if info:
                item.info = info
                item.save()
            return redirect(reverse('market:category', args=[category.id]))
        except Item.DoesNotExist:
            return HttpResponse("We don't find this item")

    @staticmethod
    @login_required
    def get_edit_item(request, id):
        return render(request, 'edit_item.html', {'id': id})


#
class AdminIncomeView(View):
    @method_decorator(login_required)
    def get(self, request):
        is_income = False
        try:
            user = request.user
            admin = Administrator.objects.get(user=user)
            stock = Stock.objects.get(admin=admin)
            items = Item.objects.filter(stock=stock, admin__isnull=True)
            context_dict = {}
            if items:
                context_dict['sold_items'] = items
                x = 0
            for i in items:
                x += i.price * i.quanity
                context_dict['income'] = x
            return render(request, 'income.html', context_dict)
        except Stock.DoesNotExist:
            return render(request, 'income.html', {'income': is_income})
