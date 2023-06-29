from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='list'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('recipe/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('recipes_search/', views.RecipeFilterView.as_view(), name='search'),
    path('recipe/detail/<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),  # noqa: E501
    path('category/<str:name>/', views.RecipeListCategoryView.as_view(), name='category'),  # noqa: E501
    path('recipe/edit/<slug:slug>/', views.RecipeUpdateView.as_view(), name='update'),  # noqa: E501
]
