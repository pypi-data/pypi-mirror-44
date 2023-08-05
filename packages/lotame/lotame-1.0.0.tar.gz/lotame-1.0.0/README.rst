| |Build Status|

Lotame API Wrapper
------------------

Wrapper Class for Lotame API.

    | Fully unit tested wrapper class for Lotame REST API.
    | https://api.lotame.com/docs
    | https://github.com/paulokuong/lotame

Requirements
------------

-  Python 3.6 (tested)

Goal
----

| To provide a generic wrapper Lotame API

Code sample
-----------

| Instantiate

.. code:: python

    from lotame import Lotame
    l = Lotame(username='xxxx', password='yyyy')

| Search audiences

.. code:: python

    audiences = l.get('audiences/search', searchTerm='Age - ').json()['Audience']

| Get behavior 3333

.. code:: python

    behavior = l.get('behaviors/{}'.format(3333)).json()

| Create audience segment with 3 behaviors.

.. code:: python

    audience_definition = l.get_create_audience_json(
        'Lotame api test 5',
        2215, [[6322283, 6322292], [6322283, 6322292]],
        'Testing out Lotame API 5')
    post_response_json = l.post('audiences', audience_definition).json()
    print(post_response_json)

 | Create audience segment with 3 behaviors for (My Profile)

.. code:: python

    audience_definition = l.get_create_audience_json(
        'Lotame api test 5',
        2215, [[6322283, 6322292, 1111760, 6322303], [6322283, 6322292, 1111760, 6322303]],
        'Testing out Lotame API 5', overlap=True)

Contributors
------------

-  Paulo Kuong (`@pkuong`_)

.. _@pkuong: https://github.com/paulokuong

.. |Build Status| image:: https://travis-ci.org/paulokuong/lotame.svg?branch=master
.. target: https://travis-ci.org/paulokuong/lotame
