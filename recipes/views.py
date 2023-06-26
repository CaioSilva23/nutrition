from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import Http404, HttpResponse
from recipes.models import Recipe
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView
from utils.pagination import make_pagination
import os
from recipes.form import RecipeForm
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

per_page = os.environ.get('PER_PAGE', 6)


def recipe_list(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
                                    request=request,
                                    queryset=recipes,
                                    per_page=per_page
                                    )
    ctx = {
        'recipes': page_obj,
        'pagination_range': pagination_range
    }
    return render(request, 'recipes/recipe_list.html', ctx)


def recipe_detail(request, slug):
    ctx = {
        'recipe': get_object_or_404(Recipe.objects.order_by('-pk'), slug=slug, is_published=True),  # noqa: E501
        'detail': True
    }
    return render(request, 'recipes/recipe_detail.html', ctx)


def recipe_list_category(request, pk):
    recipes = get_list_or_404(Recipe, category__id=pk, is_published=True)

    page_obj, pagination_range = make_pagination(
                                request=request,
                                queryset=recipes,
                                )
    ctx = {
        'recipes': page_obj,
        'pagination_range': pagination_range
    }

    return render(request, 'recipes/recipe_search_category.html', ctx)


def recipes_search(request):
    search = request.GET.get('search', '').strip()
    if not search:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(title__icontains=search) |
        Q(description__icontains=search),
        is_published=True).order_by('-pk')

    page_obj, pagination_range = make_pagination(
                                    request=request,
                                    queryset=recipes,
                                    )

    ctx = {
        'recipes': page_obj,
        'search': search,
        'pagination_range': pagination_range,
        'additional_url_query': f'&search={search}',
    }
    return render(request, 'recipes/recipe_search.html', ctx)


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipes/recipe_new.html'
    form_class = RecipeForm
    success_url = reverse_lazy('author:dashboard')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        messages.success(self.request, 'New recipe add successfull')
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_new.html'

    def get_success_url(self) -> str:
        slug = self.kwargs.get('slug')
        messages.success(self.request, 'Recipe edit successfull')
        return reverse_lazy('recipe:update', kwargs={'slug': slug})
