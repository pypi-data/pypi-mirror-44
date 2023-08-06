DirectApps
==========

This is a little application for direct access to all the models and their
data in a project. By default, the application has access for users with
`is_staff` mark. But this and much more can be changed.

It might interest you if you use Django as the backend to some kind of
external client application. There are no templates for formatting and
displaying of data on the client. Only JSON. Only direct data. All quickly and
sharply.

.. important::
    The client application must support cookies, parse "csrftoken" and send
    it as `X-CSRFToken` header in `POST`, `PUT`, `PATCH` and `DELETE` requests.

Installation
------------

.. code-block:: shell

    pip install django-directapps

Change your next project files.

.. code-block:: python

    # settins.py
    INSTALLED_APPS = (
        ...
        'directapps',
        ...
    )

    # urls.py
    urlpatterns = [
        ...
        url(r'^apps/', include('directapps.urls', namespace="directapps")),
        ...
    ]

Start the development server Django, if it is not running.

Now you can open a browser to this address to see a list of available
applications and links to data schematics for each.


Enjoy!


Using the REST API
------------------

General information
~~~~~~~~~~~~~~~~~~~

The REST API endpoints are built as follows:

.. code-block::

    /<list_apps>/<app>/<model>[.<model_using>]/<object_id>/<relation>[.<relation_using>]/<relation_id>/

You can perform actions on endpoints by specifying them with an underscore:

.. code-block::

    .../<model>[.<model_using>]/_<model_action>/
    .../<model>[.<model_using>]/<object_id>/_<object_action>/

.. code-block::

    .../<relation>[.<relation_using>]/_<relation_action>/
    .../<relation>[.<relation_using>]/<relation_id>/_<relation_object_action>/

Parameters **<model_using>** and **<relation_using>** is define a database
connection by its ID.

.. note::
    The parameter **<model_using>** is useless when you work with relations,
    but you can it remain for convenience.

For data sets (**<model>** and **<relation>**) apply the following GET-parameters::

    1. 'o' - ordering key (by default is from models definition)
    2. 'c' - columns key (by default is all from allowed)
    3. 'l' - limit key (by default is 10)
    4. 'p' - page key (by default is 1)
    5. 'q' - search key
    6. 'f' - foreign key (used in conjunction with the search key, see bellow)

All these keys can be overridden either together or separately in controller.
You can check their names in the full scheme of model.

.. note::
    Unlike many of the application with REST, a description of the data for
    client applications is not transmitted with every call, and exists as a
    separate resource, allowing you to do everything faster. This is a
    characteristic feature of this app and it means that:

    1. The client gets the list of available applications.
    2. Gets application schema which describes what data can be provided
       and on what resource they are.
    3. And only then begin to work with the data.
    4. The client application is responsible for the maintenance of relations
       between data models for fields with external links have the attribute
       "relation" that contains the full name of the relation.

Let's analyze it on the example of `django.contrib.auth` application.


Getting the scheme of available applications and models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Short scheme as list applications with version and checksum:

.. code-block::

    GET /apps/

Full scheme as list models in application:

.. code-block::

    GET /apps/auth/

.. note::
    In the response the permissions for the superuser are marked with just
    the text "all", and for other users there will be a list.


Creating the data
~~~~~~~~~~~~~~~~~

Make groups:

.. code-block::

    POST /apps/auth/group/ {'name': 'Administrators'}
    POST /apps/auth/group/_create/ {'name': 'Managers'}
    POST /apps/auth/group/_add/ {'name': 'Operators'}


Getting the data
~~~~~~~~~~~~~~~~

When you use several databases, you should use the indication of the database
from which you want to get the object. To do this, use **<model_using>** and
**<relation_using>** parameters.

Get the list users:

.. code-block::

    GET /apps/auth/user/
    GET /apps/auth/user/?o=-id,username
    GET /apps/auth/user/?o=-id&l=1
    GET /apps/auth/user/?q=blabla

.. code-block::

    GET /apps/auth/group/1/user/
    GET /apps/auth/group/1/user/?o=-id,username
    GET /apps/auth/group/1/user/?o=-id&l=1
    GET /apps/auth/group/1/user/?q=blabla

Get the user by ID=1:

.. code-block::

    GET /apps/auth/user/1/

.. code-block::

    GET /apps/auth/group/1/user/1/

Use *foreign key* for search available groups in ManyToManyField:

.. code-block::

    GET /apps/auth/user/_fkey/?f=groups
    GET /apps/auth/user/_fkey/?f=groups&q=rator
    GET /apps/auth/user/_fkey/?f=groups&q=rator&o=-id&l=1

Of course, the *foreign key* you can use with ForeignKey or OneToOneField too:

.. code-block::

    GET /apps/auth/permission/_fkey/?f=content_type

Modify data:

.. code-block::

    PATCH /apps/auth/user/1/ { first_name: 'Johnny' }
    PUT /apps/auth/user/1/ { first_name: 'John' }
    POST /apps/auth/user/1/_patch/ { first_name: 'John Bo' }
    POST /apps/auth/user/1/_put/ { first_name: 'John Bon' }
    POST /apps/auth/user/1/_update/ { last_name: 'Jovi' }

Delete data:

.. code-block::

    DELETE /apps/auth/user/1/
    POST /apps/auth/user/1/_delete/


Using in browser
----------------

You can look at the example works in the JavaScript console and use it as a test.

.. code-block:: javascript

    function getCookie(cname) {
        var name = cname + '=';
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1);
            if (c.indexOf(name) === 0) return c.substring(name.length, c.length);
        }
        return '';
    }

    function makeRequest(method, url, data, content_type) {
        var xhr = new XMLHttpRequest(),
            content_type = content_type || 'application/x-www-form-urlencoded';
        xhr.open(method, url, false);
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method.toUpperCase()))) {
            xhr.setRequestHeader('Content-Type', content_type);
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
        xhr.send(data);
        if (xhr.status === 200) return JSON.parse(xhr.responseText);
        console.error(xhr.responseText);
    }

    var group1 = makeRequest('post', '/apps/auth/group/', 'name=Operators 1'),
        group2 = makeRequest('post', '/apps/auth/group/',
                             JSON.stringify({ name: 'Operators 2' }),
                             'application/json');

    makeRequest('get', '/apps/auth/group/?o=name,-id&q=operators&p=1&l=3&id__gte=1');
    makeRequest('put', '/apps/auth/group/' + group1.pk + '/', 'name=Operators 11');
    makeRequest('patch', '/apps/auth/group/' + group2.pk + '/', 'name=Operators 22');
    makeRequest('get', '/apps/auth/group/?o=name,-id&q=operators&p=1&l=3&id__gte=1');
    makeRequest('delete', '/apps/auth/group/', 'id=' + group1.pk + ',' + group2.pk);
    makeRequest('delete', '/apps/auth/group/',
                JSON.stringify({ id: [ group1.pk, group2.pk ] }),
                'application/json');


Settings
--------

All next settings must be within the dictionary `DIRECTAPPS`, when you
define them in the file settings.py

ACCESS_FUNCTION
~~~~~~~~~~~~~~~
Function that checks access to resources.
The default is the internal function `directapps.access.staff`.
But you may want to use `directapps.access.superuser` or custom function.

ATTRIBUTE_NAME
~~~~~~~~~~~~~~
The name of the attribute in the model that is bound to the controller.
By default is `directapps_controller`.

CHECKSUM_VERSION
~~~~~~~~~~~~~~~~
The options for the checksum compilation of the scheme.
By default is `"1"`.

CONTROLLERS
~~~~~~~~~~~
Dictionary own controllers for models of third-party applications.
By default is blank.

EXCLUDE_APPS
~~~~~~~~~~~~
The list of excluded applications.
By default is blank.

EXCLUDE_MODELS
~~~~~~~~~~~~~~
The list of excluded models.
By default is blank.

JSON_DUMPS_PARAMS
~~~~~~~~~~~~~~~~~
The options for creating JSON.
By default is ``{'indent': 2, 'ensure_ascii': False}``.

MASK_PASSWORD_FIELDS
~~~~~~~~~~~~~~~~~~~~
The options for masking all the fields with the name "password".
By default is `True`.

MASTER_CONTROLLER
~~~~~~~~~~~~~~~~~
Class (as string for import) of the master controller, which is used by default.
By default is `None` and uses internal class.

USE_TIME_ISOFORMAT
~~~~~~~~~~~~~~~~~~
The options for the using ISO time with microseconds into `JSONEncoder`.
By default is `False` and `JSONEncoder` used ECMA-262 format.

SEARCH_KEY
~~~~~~~~~~
The key by which data is received for search.
By default is 'q'.

FOREIGN_KEY
~~~~~~~~~~~
The key by which the name of the field or column with a relation
(for the "_fkey" action) is received from the client.
By default is 'f'.

COLUMNS_KEY
~~~~~~~~~~~
The key by which the list of fields for rendering is received.
By default is 'c'.

ORDERING_KEY
~~~~~~~~~~~~
The key by which sorting is accepted from the client.
By default is 'o'.

LIMIT_KEY
~~~~~~~~~
The key by which the limit of records is accepted from the client.
By default is 'l'.

PAGE_KEY
~~~~~~~~
The key by which the client receives the page number.
By default is 'p'.

LIMIT
~~~~~
The global working limit of returned records.
By default is 10.

MAX_LIMIT
~~~~~~~~~
The global maximum limit of returned records, which does not allow to kill the
server with huge data sets.
By default is 50.


Customizing of controllers
--------------------------

To change the behavior globally for all your controllers, make your main
controller based on the built-in and connect it:

.. code-block:: python

    # myapp/controllers.py

    import logging
    from directapps import controllers

    logger = logging.getLogger(__name__)


    class CustomModelController(controllers.ModelController):
        # of course, your may be do it in the settings, but just for example :)
        search_key = 'search'
        limit = 50
        max_limit = 1000


    class CustomObjectController(controllers.ObjectController):

        def action_get(self, request, object, *args, **kwargs):
            logger.info(
              '%s open %s with ID=%s', request.user, self, object,
            )
            return super().action_get(request, object, *args, **kwargs)


    class CustomMasterController(controllers.MasterController):

        model_ctrl_class = CustomModelController
        object_ctrl_class = CustomObjectController


.. code-block:: python

    # settings.py

    DIRECTAPPS = {
        'MASTER_CONTROLLER': 'myapp.controllers.CustomMasterController'
    }


To change the behavior of only one controller, make your own based on the
built-in and connect it like this:

.. code-block:: python

    # myapp/controllers.py

    from django.db.models import Count
    from directapps import controllers


    class UserModelController(controllers.ModelController):
        annotations = (
            # Method or property on instance of model.
            'get_full_name',
            'get_short_name',
            # QuerySet annotation.
            'groups__count',
        )

        def get_queryset(self, *args, **kwargs):
            """Returns modified QuerySet."""
            qs = super().get_queryset(*args, **kwargs)
            qs = qs.annotate(Count('groups'))
            return qs

        def info(self, request, qs):
            """Returns information about the set. Redefined method."""
            all_users = self.get_queryset(request, using=qs.using)
            return {
                'total': all_users.count()
            }


    class UserController(controllers.MasterController):

        model_ctrl_class = UserModelController


.. code-block:: python

    # settins.py

    DIRECTAPPS = {
        'CONTROLLERS': {
            'auth.user': 'myapp.controllers.UserController',
        }
    }


Contributing
------------
If you want to translate the app into your language or to offer a more
competent application code, you can do so using the "Pull Requests" on `gitlab`_.

.. _gitlab: https://gitlab.com/djbaldey/django-directapps/
