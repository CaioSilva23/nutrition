from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from recipes.models import Recipe
from collections import defaultdict
from django.core.exceptions import ValidationError
from utils.is_positive import is_positive

class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        exclude = ('author', 'is_published', 'preparation_steps_is_html')
        widgets = {
            'cover': forms.FileInput(attrs={
                'class': 'span-2'
            }),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            )
        }

    def clean(self) -> Dict[str, Any]:
        clean = super().clean()
        if self._my_errors:
            raise ValidationError(self._my_errors)
        return clean

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 4:
            self._my_errors['title'].append('field cannot be less than 5 characters')
        return title

    def clean_servings(self):
        servings = self.cleaned_data['servings']
        if not is_positive(servings):
            self._my_errors['servings'].append('Number is required positive')
        return servings