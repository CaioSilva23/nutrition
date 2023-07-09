from django.urls import path
from .views import site as views
from .views import api

app_name = 'recipe'

# URL SITE
urlpatterns = [
    path('', views.RecipeListView.as_view(), name='list'),
    path('api/v1/', views.RecipeListViewApi.as_view(), name='list-api'),
    path('create/', views.RecipeCreateView.as_view(), name='create'),
    path('recipe/delete/', views.RecipeDeleteView.as_view(), name='delete'),
    path('recipes_search/', views.RecipeFilterView.as_view(), name='search'),
    path('recipe/tags/<slug:slug>/', views.RecipeListViewTags.as_view(), name='tags'),  # noqa: E501
    path('recipe/detail/<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),  # noqa: E501
    path('api/vi/detail/<slug:slug>/', views.RecipeDetailViewApi.as_view(), name='detail-api'),  # noqa: E501
    path('category/<str:name>/', views.RecipeListCategoryView.as_view(), name='category'),  # noqa: E501
    path('recipe/edit/<slug:slug>/', views.RecipeUpdateView.as_view(), name='update'),  # noqa: E501
]

# URL API
urlpatterns += [
    path('recipe/api/v2/', api.recipe_api_list, name='recipe_api_list'),
    path('recipe/api/v2/<int:pk>/', api.recipe_api_detail, name='recipe_api_detail'),  # noqa: E501
    path("recipe/api/v2/tag/<int:pk>/", api.recipe_api_tag_detail, name="tag_detail"),  # noqa: E501
    path('recipe/category/list/<int:pk>/', api.recipe_api_category_list, name='recipe_category_list'),  # noqa: E501
]
