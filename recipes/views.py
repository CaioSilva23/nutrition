from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from recipes.models import Recipe
from django.db.models import Q
#  from django.core.paginator import Paginator


#  'recipes': [make_recipe() for i in range(0, 10)]
def recipe_list(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    ctx = {
        'recipes': recipes
    }
    return render(request, 'recipes/recipe_list.html', ctx)


def recipe_detail(request, slug):
    ctx = {
        'recipe': get_object_or_404(Recipe.objects.order_by('-pk'), slug=slug, is_published=True),
        'detail': True
    }
    return render(request, 'recipes/recipe_detail.html', ctx)


def recipe_list_category(request, pk):
    ctx = {
        'recipes': get_list_or_404(Recipe, category__id=pk, is_published=True),
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
    ctx = {
        'recipes': recipes,
        'search': search
    }
    return render(request, 'recipes/recipe_search.html', ctx)
