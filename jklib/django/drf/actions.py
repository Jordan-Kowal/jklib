"""
Classes to make building actions/endpoints in DRF easier
Split in 2 sub-sections:
    Enums:                  Data management with enums
    Base Handlers:          The parent/base class for action handles
"""

# Built-in
from enum import Enum

# Django
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)


# --------------------------------------------------------------------------------
# > Enums
# --------------------------------------------------------------------------------
class SerializerMode(Enum):
    """
    List of available serializer modes for an action
    Refer to DynamicViewSet.get_serializer_class() to see how they resolve serializers
    """

    NONE = 1
    UNIQUE = 2
    METHOD_BASED = 3
    ROLE_BASED = 4
    ROLE_AND_METHOD_BASED = 5


# --------------------------------------------------------------------------------
# > Base Handlers
# --------------------------------------------------------------------------------
class ActionHandler:
    """
    ---------- DESCRIPTION ----------
    Custom class for processing action calls, and also provides more flexibility for action customization
    This class must be used within the DynamicViewSet class we've created

    Permissions and Serializers must be defined at the class level, respectively in 'permissions' and 'serializers'
    Both can either directly contain the value, or be a dictionary with 1 value per method (get, post, ...)

    To process the action, call the .run() method. It will either:
        Call the [.get(), .post(), ...] function based on the action method
        Fallback on the .main() function if none of the above is found

    When initialized, the instance will store all the data from the request call, making it accessible at all times
    Also provides utility with .super_view() and .run_action_from_super_view()

    ---------- HOW TO SETUP ----------
    Make sure to define the following elements:
        serializer_mode (NONE, UNIQUE, METHOD_BASED, ROLE_BASED, ROLE_AND_METHOD_BASED)
        serializer
            if NONE                     -->     returns None
            if UNIQUE                   -->     directly returns a serializer
            if METHOD_BASED             -->     dict where each method has a serializer
            if ROLE_BASED               -->     dict with a different serializer for "user" and for "admin"
            if ROLE_AND_METHOD_BASED    -->     dict with user/admin, then methods for serializers
        [.get(), .post(), ...] if your action has several valid protocol/methods
        .main() if your action has a single method

    ---------- HOW TO USE: with DynamicViewSet ----------
    Simply match your actions with your ActionHandler classes, as described in the DynamicViewSet documentation
    The viewset will then take care of the rest
    """

    serializer_mode = SerializerMode.UNIQUE
    serializer = None

    def __init__(self, viewset, request, *args, **kwargs):
        """
        Initialize the instance  and sets up its attributes for later use
        :param ViewSet viewset: Viewset from DRF where our action will take place
        :param HttpRequest request: The request object from django that called our action
        :param args: Additional args automatically passed to our action
        :param kwargs: Additional kwargs automatically passed to our action
        """
        # Storing args
        self.viewset = viewset
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # Useful shortcuts
        self.user = request.user
        self.data = request.data
        self.method = request.method.lower()

    def run(self):
        """
        Process the service request by calling the appropriate method
        It will look for a function matching the [method] name and will default to the "main" function
        :return: Response instance from DRF, containing our results
        :rtype: Response
        """
        action_to_run = getattr(self, self.method, self.main)
        return action_to_run()

    def run_action_from_super_view(self, action_name):
        """
        Calls an action from the parent viewset with the initial arguments
        :param str action_name: Name of the method to call from the parent viewset
        :return: The results from the parent function we called
        """
        parent_viewset_action = getattr(self.super_view(), action_name)
        return parent_viewset_action(self.request, *self.args, **self.kwargs)

    def super_view(self):
        """
        Equivalent to calling super() on the viewset
        :return: The parent class of the viewset
        :rtype: ViewSet
        """
        return super(type(self.viewset), self.viewset)

    @staticmethod
    def main():
        """Default function for the service processing"""
        return MethodNotAllowed()

    def get_serializer(self, *args, **kwargs):
        """
        Shortcut to get the serializer from the viewset
        :return: The serializer attached to our current action
        :rtype: Serializer
        """
        return self.viewset.get_serializer(*args, **kwargs)

    def get_valid_serializer(self, *args, **kwargs):
        """
        Shortcut to get and validate the serializer from the viewset
        :return: The validated serializer attached to our current action
        :rtype: Serializer
        """
        return self.viewset.get_valid_serializer(*args, **kwargs)


class ModelActionHandler(ActionHandler):
    """
    Extension of ActionHandler that provides utility for Model-related viewset actions
    Includes all the CRUD functions equivalent to the DRF viewset model mixins
    """

    def get_object(self):
        """
        Shortcut to fetch an model instance
        :return: A Django instance model
        :rtype: Model
        """
        return self.viewset.get_object()

    def model_create(self):
        """
        Creates and saves a model instance
        :return: HTTP 200 with the created instance data
        :rtype: Response
        """
        serializer = self.get_valid_serializer(data=self.data)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    def model_retrieve(self):
        """
        Fetches a single model instance based on the provided serializer
        :return: HTTP 200 with the instance data
        :rtype: Response
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)

    def model_list(self):
        """
        Fetches, filters, paginates, and returns a list of instances for a given model
        :return: HTTP 200 with the list of instances
        :rtype: Response
        """
        viewset = self.viewset
        queryset = viewset.filter_queryset(viewset.get_queryset())
        page = viewset.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return viewset.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def model_update(self):
        """
        Updates and saves a model instance using the provided serializer
        :return: HTTP 200 with the updated instance data
        :rtype: Response
        """
        partial = self.kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=self.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Invalidate the pre-fetched cache if it had been applied
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data, status=HTTP_200_OK)

    def model_partial_update(self):
        """
        Sets the 'partial' kwarg to partial before calling the .model_update() method
        :return: HTTP 200 with the partially updated instance data
        :rtype: Response
        """
        self.kwargs["partial"] = True
        return self.model_update()

    def model_destroy(self):
        """
        Deletes a model instance from the database
        :return: HTTP 204 response without data
        :rtype: Response
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def model_bulk_destroy(self):
        """
        Filters the viewset queryset with the provided IDs and removes the instances found
        Expects the serializer to have an "ids" list field
        :return: HTTP 204 response without data
        :rtype: Response
        """
        serializer = self.get_valid_serializer(data=self.data)
        ids_to_delete = serializer.validated_data.pop("ids")
        instances = self.viewset.get_queryset().filter(id__in=ids_to_delete)
        if len(instances) == 0:
            return Response(None, status=HTTP_404_NOT_FOUND)
        else:
            instances.delete()
            return Response(None, status=HTTP_204_NO_CONTENT)
