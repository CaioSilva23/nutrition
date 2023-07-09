from rest_framework import serializers
from recipes.models import Recipe, Category
from tag.models import Tag
from django.contrib.auth.models import User
from collections import defaultdict
from utils.is_positive import is_positive


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'title',
            'description',
            # 'preparation',
            'servings',
            # 'servings_',
            'servings_unit',
            'preparation_time',
            'preparation_time_unit',
            'preparation_steps',
            'created_at',
            'cover',
            'category_object',
            'author_object',
            'tag_objects',
            'tag_links',
            )

    # preparation = serializers.SerializerMethodField(read_only=True)
    # servings_ = serializers.SerializerMethodField(read_only=True)
    author_object = UserSerializer(source='author', read_only=True)
    category_object = CategorySerializer(many=False, source='category', read_only=True)  # noqa: E501
    tag_objects = TagSerializer(many=True, source='tags', read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipe:tag_detail',
        read_only=True
    )

    # def get_preparation(self, recipe):
    #     return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    # def get_servings_(self, recipe):
    #     return f'{recipe.servings} {recipe.servings_unit}'

    def validate(self, attrs):

        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        title = attrs['title']
        servings = attrs.get('servings', '')

        if len(title) < 4:
            self._my_errors['title'].append('field cannot be less than 5 characters')  # noqa: E501

        if not is_positive(servings):
            self._my_errors['servings'].append('Number is required positive')

        if self._my_errors:
            raise serializers.ValidationError(self._my_errors)
        return attrs
