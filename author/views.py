from django.forms.models import BaseModelForm
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, View, ListView, TemplateView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.models import Recipe
from author.models import Profile

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
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect(reverse('author:login'))


class DashboardView(LoginRequiredMixin, ListView):
    login_url = 'author:login'
    template_name = 'author/dashboard.html'
    model = Recipe
    context_object_name = 'recipes'

    def get_queryset(self):
        recipes = Recipe.objects.filter(
            author=self.request.user,
            is_published=False)
        return recipes


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        print('USERR', user.profile.pk)
        profile = get_object_or_404(Profile.objects.filter(pk=self.kwargs['pk']).prefetch_related('author'),
                                    id=self.kwargs['pk'])
        return render(request, 'author/profile.html', context={'profile': profile})
