from django.shortcuts import render, redirect
from django.views import View  # Import the View class from django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from teacherapp.models import CustomUser


# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'accountapp/login_page.html')

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username, password=password)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        return redirect('login')


class RegisterView(View):

    def get(self, request):
        return render(request, 'accountapp/register_page.html')

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        if password == repassword:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return render(request, 'accountapp/register_page.html',)
            else:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return render(request, 'accountapp/register_page.html',)

                else:
                    user = CustomUser.objects.create_user(
                        username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                    user.save()
                    messages.success(request, 'User created successfully')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'accountapp/register_page.html',)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')
