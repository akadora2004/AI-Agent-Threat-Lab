from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from grader import evaluate_report

@login_required
def index(request):
    """
    課題提出画面
    ログイン済みのユーザーのみアクセス可能
    """
    score = None
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        if user_input:
            score = evaluate_report(user_input, request.user)
    return render(request, 'main/index.html', {'score': score})

def signup_view(request):
    """
    新規登録画面
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name', '')
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    """
    ログイン画面
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    """
    ログアウト処理
    """
    logout(request)
    return redirect('login')
