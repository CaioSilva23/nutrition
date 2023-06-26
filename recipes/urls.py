from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.recipe_list, name='list'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='detail'),
    path('category/<int:pk>/', views.recipe_list_category, name='category'),
    path('recipes_search/', views.recipes_search, name='search'),
    # crud recipe
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('recipe/edit/<slug:slug>/', views.RecipeUpdateView.as_view(), name='update'),
    # path('recipe/delete/<slug:slug>/', views.RecipeDeleteView.as_view(), name='delete'),
]
