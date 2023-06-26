from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, View, ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.models import Recipe


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'author/register.html'
    success_url = reverse_lazy('author:login')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        return super().form_valid(form)


class LoginView(View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        return render(self.request, 'author/login.html', {'form': form})

    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(self.request, user)
                messages.success(self.request, 'Usuario logado!')
                return redirect(reverse('author:dashboard'))
        messages.error(self.request, 'Error, dados incorretos !')
        return render(self.request, 'author/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    login_url = 'author:login'

    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('author:login'))


class DashboardView(LoginRequiredMixin, ListView):
    login_url = 'author:login'
    template_name = 'author/dashboard.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self) -> QuerySet[Any]:
        recipes = Recipe.objects.filter(
            author=self.request.user,
            is_published=False)
        return recipes


