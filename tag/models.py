from django.db import models
from django.utils.text import slugify
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey
import string
from random import SystemRandom


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # # campos para relação generica
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.CharField(max_length=30)
    # content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    # LETRAS A a Z         # NÚMEROS 0 a 9
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )

            self.slug = slugify(f'{self.name}-{rand_letters}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
