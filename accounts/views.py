from django.contrib.auth import (
    authenticate,
    login,
    logout,)
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,)
from django.shortcuts import (
    render,
    redirect,)


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login_page')
    context = {
        'title': 'Регистрация',
        'form': form,
    }
    return render(request, 'registration.html', context=context)


def logIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = AuthenticationForm()
    context = {
        'title': 'Вход в аккаунт',
        'form': form
    }
    return render(request, 'login.html', context=context)


def logOut(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home_page')
    context = {
        'title': 'Выход из системы'
    }
    return render(request, 'logout.html', context=context)
