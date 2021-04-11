"""Utilities for testing Django models"""

# Django
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Local
from ..utils.tests import ImprovedTestCase


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ModelTestCase(ImprovedTestCase):
    """Extends ImprovedTestCase to provide specific utility for testing Django models"""

    model_class = None

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    @property
    def common_errors(self):
        """
        :return: A list of common error classes
        :rtype: ValueError, ValidationError, IntegrityError
        """
        return ValueError, ValidationError, IntegrityError

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    def assert_instance_count_equals(self, n):
        """Tests the number of instances in the database for our model"""
        assert self.model_class.objects.count() == n
