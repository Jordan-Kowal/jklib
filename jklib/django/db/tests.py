"""Utilities for testing Django models"""

# Local
from ..utils.tests import ImprovedTestCase


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ModelTestCase(ImprovedTestCase):
    """Extends ImprovedTestCase to provide specific utility for testing Django models"""

    model_class = None

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    def assert_instance_count_equals(self, n):
        """Tests the number of instances in the database for our model"""
        assert self.model_class.objects.count() == n
