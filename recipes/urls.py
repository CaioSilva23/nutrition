from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.recipe_list, name='list'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('recipe/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('recipes_search/', views.recipes_search, name='search'),
    path('recipe/detail/<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),
    path('category/<int:pk>/', views.recipe_list_category, name='category'),
    path('recipe/edit/<slug:slug>/', views.RecipeUpdateView.as_view(), name='update'),
]
