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

from .forms import DesignRequest

@login_required
def profile(request):
    user_requests = DesignRequest.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'user_requests': user_requests})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm
from django.contrib import messages

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'main/create_request.html', {'form': form})

from django.shortcuts import get_object_or_404

@login_required
def delete_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)
    if request.method == 'POST':
        design_request.delete()
        messages.success(request, "Заявка успешно удалена!")
        return redirect('profile')