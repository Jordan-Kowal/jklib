"""Utilities for testing Django models"""

# Built-in
from typing import Type

# Django
from django.db.models import Model

# Local
from ..utils.tests import ImprovedTestCase


class ModelTestCase(ImprovedTestCase):
    """Extends ImprovedTestCase to provide specific utility for testing Django models"""

    def assert_instance_count(self, model: Type[Model], n: int) -> None:
        self.assertEqual(model.objects.count(), n)
