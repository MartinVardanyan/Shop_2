from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from market.forms import CustomerForm
from market.models import Customer, Stock, Category, Item, MyBug
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
        my_bug = MyBug.objects.filter(customer=customer)
        print(customer, 2)
        context_dict = {}
        context_dict['customer'] = customer
        context_dict['my_bug'] = my_bug
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


class CustomerAddItemMyBugView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        item = Item.objects.get(id=id)
        print('get', item)
        return render(request, 'add_my_bug.html')

    @method_decorator(login_required)
    def post(self, request, id):
        add = False
        print('post')
        if request.method == 'POST':
            print(1)
            user = request.user
            customer = Customer.objects.get(user=user)
            item = Item.objects.get(id=id)
            item.quanity = item.quanity - int(request.POST.get('quanity'))
            item.save()
            print(2, item)
            my_bug = MyBug()
            my_bug.customer = customer # Hajord toxic anhaskanliya, vonc anem quanity pahy - ???!!!
            item.quanity = request.POST.get('quanity')
            print(my_bug.item)
            my_bug.save()
            print(3, my_bug)
            add = True
            return render(request, 'add_my_bug.html', {'add': add,
                                                       'item': item})
        else:
            return render(request, 'item_list.html', {'add': add})


class CustomerMyBugView(View):
    @method_decorator(login_required)
    def get(self, request):
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

    @method_decorator(login_required)
    def post(self, request):
        print('post')
        return render(request, 'my_bug.html')

# Erb sa verchacnenq, liqy baner karelia avelacnel, orinak Itemi ej vor sxmes, itemi vra ira masin info beri
# Kam yete mardy nshuma ynqan qanak apranqi, ynqan xanuty chuni, inqy avtomat cuyc ta, mecaguyn qanaqy, ynqan arka e xanutum, ev avel ch toxni!
# Evs mi banel orinak avelacnelu functionalutyuny sarqel, vochty arandzin ejow, ay amen apranqi koxy qanaq nshelu hnaraworutyun tal,
# ev koxqy vorpes buttom MyBug avelacnelu hnaravorutyun!!!
# Searchi hnaravorutyun itemneri ej, bayc et miqich djvar k lini, search-i het liqy ban ka, vory karelia anel, tarasxalner, angleren, mecatar, poqratar ev ayl
# Kam search-y kazmakerpel filtreneri mijocow
# Apranqner kan voronq hatow chen, ayl qashowen, et harcy chgitem, vonc karelia kazmakerpel
