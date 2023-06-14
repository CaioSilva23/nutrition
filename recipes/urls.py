from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.recipe_list, name='list'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='detail'),
    path('category/<int:pk>/', views.recipe_list_category, name='category'),
    path('recipes_search/', views.recipes_search, name='search'),
]
