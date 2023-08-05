.. image:: https://travis-ci.org/apirobot/django-rest-action-permissions.svg?branch=master
    :target: https://travis-ci.org/apirobot/django-rest-action-permissions

.. image:: https://codecov.io/gh/apirobot/django-rest-action-permissions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/apirobot/django-rest-action-permissions

.. image:: https://badge.fury.io/py/django-rest-action-permissions.svg
    :target: https://badge.fury.io/py/django-rest-action-permissions


==============================
Django REST Action Permissions
==============================

``django-rest-action-permissions`` allows you to define permissions for each action provided by your ViewSet class.


Installation
------------

Install using pip:

.. code-block:: bash

    $ pip install django-rest-action-permissions


Usage
-----

This library lets you define permissions like so:

.. code-block:: python

    # permissions.py
    from rest_framework.permissions import (
        AllowAny, BasePermission, IsAdminUser, IsAuthenticated
    )
    from rest_action_permissions.permissions import ActionPermission


    class IsTweetOwner(BasePermission):

        def has_object_permission(self, request, view, obj):
            return obj.owner == request.user


    class TweetPermission(ActionPermission):
        # The admin user has all permissions.
        enough_perms = IsAdminUser

        # Corresponding permissions for each action.
        create_perms = IsAuthenticated
        retrieve_perms = AllowAny
        list_perms = AllowAny
        update_perms = IsTweetOwner
        delete_perms = IsTweetOwner
        retweet_perms = IsAuthenticated
        undo_retweet_perms = IsAuthenticated

        # General read/write permissions.
        # Used if corresponding action permission hasn't been specified.
        read_perms = AllowAny
        write_perms = IsAuthenticated & IsTweetOwner


Corresponding ViewSet for the permissions defined above:

.. code-block:: python

    # views.py
    from rest_framework import viewsets
    from rest_framework.decorators import detail_route
    from .models import Tweet
    from .permissions import TweetPermission
    from .serializers import TweetSerializer


    class TweetViewSet(viewsets.ModelViewSet):
        queryset = Tweet.objects.all()
        serializer_class = TweetSerializer
        permission_classes = (TweetPermission, )

        def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

        @detail_route(methods=['POST'])
        def retweet(self, request, *args, **kwargs):
            ...

        @detail_route(methods=['POST'])
        def undo_retweet(self, request, *args, **kwargs):
            ...


Credits
-------

The interface of this library was inspired by `taiga <https://github.com/taigaio/taiga-back>`_ project.
