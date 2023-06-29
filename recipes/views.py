from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from django.http import Http404, HttpRequest, HttpResponse
from recipes.models import Recipe
from django.db.models import Q
from django.views.generic import View, CreateView, UpdateView, DetailView, ListView  # noqa: E501
from utils.pagination import make_pagination
import os
from recipes.form import RecipeForm
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

per_page = os.environ.get('PER_PAGE', 6)


class RecipeListBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ('-id',)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
                                    request=self.request,
                                    queryset=ctx.get('recipes'),
                                    per_page=per_page
                                    )
        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})
        return ctx


class RecipeListView(RecipeListBase):
    template_name = 'recipes/recipe_list.html'


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({'detail': True})
        return ctx

    def get_queryset(self):
        return Recipe.objects.filter(slug=self.kwargs['slug'], is_published=True)  # noqa: E501


class RecipeListCategoryView(RecipeListBase):
    template_name = 'recipes/recipe_list_category.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        return qs.filter(category__name=self.kwargs['name'])


class RecipeFilterView(RecipeListBase):
    template_name = 'recipe_search.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        self.search = self.request.GET.get('search', '').strip()

        if not self.search:
            raise Http404()

        qs = qs.filter(
            Q(title__icontains=self.search) | Q(description__icontains=self.search),  # noqa: E501
            is_published=True)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'search': self.search,
            'additional_url_query': f'&search={self.search}',
        })
        return ctx


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

    def get_queryset(self):
        recipe = Recipe.objects.filter(is_published=False, author=self.request.user)  # noqa: E501
        return recipe


class RecipeDeleteView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        slug = self.request.POST.get('slug')
        recipe = Recipe.objects.filter(
            slug=slug,
            is_published=False,
            author=self.request.user).first()  # noqa: E501
        if recipe:
            recipe.delete()
            messages.success(self.request, 'Receita deletada com sucesso!')
            return redirect(reverse('author:dashboard'))
        messages.error(self.request, 'Esta receita não é sua ou não existe!!!')
        return redirect(reverse('author:dashboard'))
