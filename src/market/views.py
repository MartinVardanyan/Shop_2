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
                print("Invalid login details: {0}, {1}".format(username, password))
        else:
            render(request, 'login.html')


class Logout_View(View): # the same as LoginView
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect(reverse('market:login'))
