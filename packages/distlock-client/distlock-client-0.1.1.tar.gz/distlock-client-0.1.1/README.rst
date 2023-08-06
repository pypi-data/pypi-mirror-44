distlock-client
===============

.. image:: https://travis-ci.org/appstore-zencore/distlock-client.svg?branch=master
    :target: https://travis-ci.org/appstore-zencore/distlock-client

.. image:: https://img.shields.io/codecov/c/github/appstore-zencore/distlock-client.svg?style=flat-square
    :target: https://codecov.io/gh/appstore-zencore/distlock-client


Distribute lock system's client.


Install
-------

::

    pip install distlock-client


Usage
-----

1. Use Lock apis.

::

    from distlock_client import Lock
    from distlock_client import get_app_unique_name
    from .services import do_something

    def view01(request):
        lockName = "view01_lock"
        appid = get_app_unique_name()
        server = "http://127.0.0.1/"
        lock = Lock(appid, server)

        locked = lock.safe_acquire(lockName, 60)
        if locked:
            try:
                do_something()
            finally:
                lock.safe_release(lockName)


2. Use with statement.

::

    from distlock_client import Lock
    from distlock_client import distlock
    from distlock_client import get_app_unique_name
    from .services import do_something

    def view01(request):
        lockName = "view01_lock"
        appid = get_app_unique_name()
        server = "http://127.0.0.1/"
        lock = Lock(appid, server)
        with distlock(lock, lockName) as locked:
            if locked:
                do_something()

Misc
----

1. Available servers.

  - django-distlock-server [python, django, database backend]
  - django-distlock-server-redis [python, django, redis backend]

