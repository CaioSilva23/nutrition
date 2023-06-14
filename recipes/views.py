from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Recipe
from django.urls import reverse


# 'recipes': [make_recipe() for i in range(0, 10)]
def recipe_list(request):
    ctx = {
        'recipes': Recipe.objects.filter(is_published=True)
    }
    return render(request, 'recipes/recipe_list.html', ctx)


def recipe_detail(request, pk):
    ctx = {
        'recipe': get_object_or_404(Recipe, id=pk, is_published=True),
        'detail': True
    }
    return render(request, 'recipes/recipe_detail.html', ctx)


def category_list(request, pk):
    ctx = {
        'recipes': get_list_or_404(Recipe, category__id=pk, is_published=True)
    }

    return render(request, 'recipes/recipe_list.html', ctx)
