Froi (Flask Router Object Interface)
====================================

A wrapper for Flask's native routing as a form of template.
Routes will be defined as objects to easily define domains.

.. code-block:: python

    # Inside some route object
    from froi import Froi
    class SomeRoute(Froi):
        def __init__(self, app):
            super().__init__(app, 'SomeRoute', '/some_route')

        def install(self):
            # define a get route on base
            self.setget().route(view_func=sample_fxn_1)

            # define a post
            self.setpost().route('/do_something', view_func=sample_fxn_2)

            # define a put
            self.setput().route('/edit_something', view_func=sample_fxn_3)

            # define a delete
            self.setdelete().route('/delete_something', view_func=sample_fxn_4)

    # Inside your server handler
    from flask import Flask
    from some_route import SomeRoute
    app = Flask(config.APP_NAME)
    SomeRoute(app).install()
    app.run()

If you want a RESTful pattern to handle the routes, you can omit defining the `install` function.

.. code-block:: python

    from froi import Froi
    class SomeRoute(Froi):
        def __init__(self, app):
            super().__init__(app, 'SomeRoute', '/some_route')

        def get(self):
            ... do something

        def post(self):
            ... do something

This will automatically create the defined `GET`, `POST`, `PUT`, and `DELETE` endpoints.
