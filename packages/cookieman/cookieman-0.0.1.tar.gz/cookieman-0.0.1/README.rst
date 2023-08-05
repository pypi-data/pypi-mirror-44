cookieman
=========

Browser-aware flask session manager.

This module allows you to store any amount of data on session cookies without
caring about browser-specific cookie limitations, by just registering session
data shrink functions.

This module probably won't play nicely with other cookies set on the same
domain: session-cookie could be evicted at any time because other cookies and
vice versa.

How it works
------------

This module includes a simple browser cookie limit database, which is matched
against flask request's user agent and, on flask response, that information
is used to serialize the session onto cookies.

This session implementation supports cookie signatures, multi-cookie session,
and custom session shrinking logic which will be invoked when needed.

The session shrinking logic repeat this steps in order until session data fits
into cookies:

1. Registered shrinking functions, until they're unable to reduce the cookie
   size.
2. Unhandled keys are removed.
3. Registered shrinking functions, now receiving ``True`` as parameter
   ``last``.
4. Remaining keys are removed.

Usage
-----

This module works as a flask session interface, allowing to register session
shrink functions which will be called once session does not fit on browser
cookies.

.. code:: python

    import flask
    import cookieman

    app = flask.Flask(__name__)
    app.session_interface = cookieman.CookieMan()
    app.secret_key = 'my_app_secret_key'  # used for session cookie safety

    @app.session_interface.register('a')
    def shrink_a(data, last):
        '''
        Session property 'a' shrinking policy: remove last list item on key
        or just remove key.

        :param data: session data as dict
        :type data: Mapping[str, Any]
        :param last: wether is last iteration or not
        :type last: bool
        :returns: updated data (can be the same as received)
        :rtype: Mapping[str, Any]
        '''
        if len(data['a']) < 2:
            del data['a']
        else:
            data['a'].pop()
        return data

License
-------
MIT (see LICENSE file).
