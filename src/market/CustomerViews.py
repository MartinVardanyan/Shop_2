from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from market.forms import CustomerForm
from market.models import Customer


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