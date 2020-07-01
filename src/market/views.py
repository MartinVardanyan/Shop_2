from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from market.models import Administrator
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if Administrator.objects.filter(user=user):
                    login(request, user)
                    return redirect(reverse('market:admin_profile'))
                else:
                    login(request, user)
                    return redirect(reverse('market:customer_profile'))
            else:
                return redirect(reverse('market:login'))
        else:
            render(request, 'login.html')


class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect(reverse('market:login'))


class AdminAboutView(View):
    @staticmethod
    def get(request):
        print('about')
        return render(request, 'about_for_admin.html')


class CustomerAboutView(View):
    @staticmethod
    def get(request):
        print('about')
        return render(request, 'about_for_customer.html')


class AdminContactsView(View):
    @staticmethod
    def get(request):
        print('contact')
        return render(request, 'contacts_for_admin.html')


class CustomerContactsView(View):
    @staticmethod
    def get(request):
        print('contact')
        return render(request, 'contacts_for_customer.html')
