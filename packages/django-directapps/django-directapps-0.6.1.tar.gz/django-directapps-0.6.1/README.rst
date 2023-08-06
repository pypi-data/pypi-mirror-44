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

Note, unlike many of the application with REST, a description of the data for
client applications is not transmitted with every call, and exists as a
separate resource, allowing you to do everything faster. This means that:

1. The client gets the list of available applications.
2. Gets application schema which describes what data can be provided and
   on what resource they are.
3. And only then begin to work with the data.
4. The client application is responsible for the maintenance of relations
   between data models for fields with external links have the attribute
   "relation" that contains the full name of the relation.

Enjoy!

Testing
-------

You can look at the example works in the JavaScript console and use it as a test.

.. code-block:: javascript

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
        }
        return "";
    }

    function getResponse(method, url, data, content_type) {
        var xhr = new XMLHttpRequest(),
            content_type = content_type || 'application/x-www-form-urlencoded';
        xhr.open(method, url, false);
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method.toUpperCase()))) {
            xhr.setRequestHeader('Content-Type', content_type);
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
        xhr.send(data);
        if (xhr.status == 200) return JSON.parse(xhr.responseText);
        console.error(xhr.responseText);
    }

    var group1 = getResponse('post', '/apps/auth/group/', 'name=Operators 1'),
        group2 = getResponse('post', '/apps/auth/group/',
                             JSON.stringify({name: 'Operators 2'}),
                             'application/json');

    getResponse('get', '/apps/auth/group/?o=name,-id&q=operators&p=1&l=3&id__gte=1');
    getResponse('put', '/apps/auth/group/'+group1.pk+'/', 'name=Operators 11');
    getResponse('patch', '/apps/auth/group/'+group2.pk+'/', 'name=Operators 22');
    getResponse('get', '/apps/auth/group/?o=name,-id&q=operators&p=1&l=3&id__gte=1');
    getResponse('delete', '/apps/auth/group/', 'id='+group1.pk+','+group2.pk);
    getResponse('delete', '/apps/auth/group/',
                JSON.stringify({id: [group1.pk, group2.pk]}),
                'application/json');


Settings
--------

All next settings must be within the dictionary `DIRECTAPPS`, when you
define them in the file settings.py

ATTRIBUTE_NAME
~~~~~~~~~~~~~~
The name of the attribute in the model that is bound to the controller.
By default is `directapps_controller`.

MASTER_CONTROLLER
~~~~~~~~~~~~~~~~~
Class (as string for import) of the master controller, which is used by default.
By default is `None` and uses internal class.

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

ACCESS_FUNCTION
~~~~~~~~~~~~~~~
Function that checks access to resources.
By default is `None` and uses internal function.

JSON_DUMPS_PARAMS
~~~~~~~~~~~~~~~~~
The options for creating JSON.
By default is ``{'indent': 2, 'ensure_ascii': False}``.

MASK_PASSWORD_FIELDS
~~~~~~~~~~~~~~~~~~~~
The options for masking all the fields with the name "password".
By default is `True`.

CHECKSUM_VERSION
~~~~~~~~~~~~~~~~
The options for the checksum compilation of the scheme.
By default is `"1"`.

USE_TIME_ISOFORMAT
~~~~~~~~~~~~~~~~~~
The options for the using ISO time with microseconds into `JSONEncoder`.
By default is `False` and `JSONEncoder` used ECMA-262 format.


Contributing
------------
If you want to translate the app into your language or to offer a more
competent application code, you can do so using the "Pull Requests" on `gitlab`_.

.. _gitlab: https://gitlab.com/djbaldey/django-directapps/
