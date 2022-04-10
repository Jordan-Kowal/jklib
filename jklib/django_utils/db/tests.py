"""Utilities for testing Django models"""

# Built-in
from typing import Type

# Django
from django.db.models import Model

# Local
from ..utils.tests import ImprovedTestCase


class ModelTestCase(ImprovedTestCase):
    """Extends ImprovedTestCase to provide specific utility for testing Django models"""

    def assert_instance_count_equals(self, model: Type[Model], n: int) -> None:
        """Tests the number of instances in the database for our model"""
        self.assertEquals(model.objects.count(), n)  # type: ignore
