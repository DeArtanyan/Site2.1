from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

from django.shortcuts import render
from .models import DesignRequest


def home(request):
    message = None
    if request.user.is_authenticated:
        message = "Вы успешно вошли на главную страницу."

        completed_requests = DesignRequest.objects.filter(status='completed').order_by('-id')[:4]

        in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    else:
        completed_requests = None
        in_progress_count = 0

    return render(request, 'main/home.html', {
        'message': message,
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count,
    })


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

from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    selected_status = request.GET.get('status')

    if selected_status:
        user_requests = DesignRequest.objects.filter(user=request.user, status=selected_status)
    else:
        user_requests = DesignRequest.objects.filter(user=request.user)

    return render(request, 'main/profile.html', {
        'user_requests': user_requests,
        'selected_status': selected_status,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RequestForm

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user
            design_request.status = 'new'
            design_request.save()
            messages.success(request, "Заявка успешно создана!")
            return redirect('profile')
    else:
        form = RequestForm()
    return render(request, 'main/create_request.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import DesignRequest

@login_required
def delete_request(request, request_id):
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user)
    if design_request.status in ['in_progress', 'completed']:
        messages.error(request, "Вы не можете удалить заявку, которая находится в работе или завершена.")
    elif request.method == 'POST':
        design_request.delete()
        messages.success(request, "Заявка успешно удалена.")
    return redirect('profile')

