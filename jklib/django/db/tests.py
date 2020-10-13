"""Useful constants, functions, and classes for testing Django models"""


# Django
from django.db import IntegrityError, transaction

# Local
from ..utils.tests import ImprovedTestCase


# --------------------------------------------------------------------------------
# > Classes
# --------------------------------------------------------------------------------
class ModelTestCase(ImprovedTestCase):
    """
    TestCase class specifically for testing our models
    Inherits from ImprovedTestCase
    Provides the following:
        Assertions for field constraints (unique, required, choices, etc.)
    """

    # ----------------------------------------
    # Properties
    # ----------------------------------------
    model_class = None

    # ----------------------------------------
    # Assertions
    # ----------------------------------------
    def assert_fields_are_required(self, valid_payload, fields=None):
        """
        Tests that the required fields are truly required
        For each field, we will:
            Use a valid payload
            Remove only the specific field
            Try to create the object
        :param dict valid_payload: A valid payload for the service
        :param [str] fields: List of fields to check. Defaults to self.required_fields
        """
        with transaction.atomic():
            if fields is None:
                fields = self.required_fields
            for field in fields:
                payload = valid_payload.copy()
                payload[field] = None
                with self.assertRaises(IntegrityError):
                    self.model_class(**payload).save()

    def assert_instance_count_equals(self, n):
        """Tests the number of instances in the database for our model"""
        assert self.model_class.objects.count() == n
