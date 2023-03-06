# Built-in
from typing import Any, Dict

# Django
from django.db.models import Model, QuerySet
from django_filters import FilterSet


class ImprovedFilterSet(FilterSet):
    @staticmethod
    def do_nothing(
        queryset: QuerySet[Model], _name: str, _value: str
    ) -> QuerySet[Model]:
        return queryset

    @property
    def validated_data(self) -> Dict[str, Any]:
        return self.form.cleaned_data
