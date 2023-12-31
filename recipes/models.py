from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tag.models import Tag
from django.conf import settings
from PIL import Image
import os
from django.utils.text import slugify
import string
from random import SystemRandom


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name


class RecipeManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True)\
            .order_by('-id')\
            .select_related('author', 'category')\
            .prefetch_related('tags')\



class Recipe(models.Model):
    objects = RecipeManager()

    title = models.CharField(max_length=65, unique=True)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField(blank=True)
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self) -> str:
        return f'{self.title}'
    
    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    # LETRAS A a Z         # NÚMEROS 0 a 9
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 800)
            except FileNotFoundError:
                ...

        return saved
