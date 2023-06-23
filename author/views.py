from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, 'Successfully registered user')
            return redirect('/auth/register/')
        messages.error(request, 'Incorrect data')
        return render(request, 'author/register.html', {'form': form})
    elif request.method == 'GET':
        form = RegisterForm()
        return render(request, 'author/register.html', {'form': form})

