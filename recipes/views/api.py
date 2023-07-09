from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..serializers import RecipeSerializer, TagSerializer
from ..models import Recipe
from tag.models import Tag
from django.shortcuts import get_object_or_404


@api_view(http_method_names=['get', 'post'])  # 
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
            )
        return Response(
            data={'recipes': serializer.data},
            status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=1, category_id=1, tags=[1, 2]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):

    recipe = get_object_or_404(Recipe.objects.get_published(), pk=pk,)

    if request.method == 'GET':
        serializer = RecipeSerializer(instance=recipe)
        return Response(
            data={'recipe': serializer.data},
            status=status.HTTP_200_OK)  # noqa: E501

    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            data=request.data,
            instance=recipe,
            context={'request': request},
            partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'recipe': serializer.data}, status=status.HTTP_200_OK)  # noqa: E501

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def recipe_api_tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(instance=tag, many=False)
    return Response(data=serializer.data)
