from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login


def home(request):
    message = None
    if request.user.is_authenticated:
        message = "Вы успешно вошли на главную страницу."
    return render(request, 'main/home.html', {'message': message})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрированы. Пожалуйста, войдите в систему.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Не правильный логин или пароль")
    return render(request, 'main/login.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from django.contrib import messages

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'main/create_request.html', {'form': form})