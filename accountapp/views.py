from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from accountapp.models import Student
from .forms import RegistrationForm
from django.contrib import messages
from django.views import View


class RegisterView(View):  # RegisterView from UserCreationForm
    def get(self, request):
        form = RegistrationForm()

        context = {
            'form': form
        }
        return render(request, 'accountapp/register_page.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            messages.success(request, 'Registration Successful.')
            return redirect('login')
        else:
            context = {
                'form': form
            }
            return render(request, 'accountapp/register_page.html', context)


class LoginView(View):  # LoginView from AuthenticationForm
    def get(self, request):

        form = AuthenticationForm()
        context = {
            'form': form
        }

        return render(request, 'accountapp/login_page.html', context)

    def post(self, request):

        form = AuthenticationForm(request.POST, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:

            context = {
                'form': form
            }
            return render(request, 'accountapp/login_page.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')
