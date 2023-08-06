django-dbcron
=============

Manage crontab directly from your Django database

Why
---

They are plenty of implementation of crontabs in Python and Django, but our
issue was their elasticity. Generally a set of classes will allow you to
create a crontab, here in django-dbcron, things are stored in database
instead of Python classes.


Installation
------------

Classic pip install: ::

  pip install django-dbcron


Add it to you ``INSTALLED_APPS``: ::

  INSTALLED_APPS = (
    ...
    'dbcron',
    ...
  )

Launch migrations: ::

  ./manage.py migrate dbcron

Usage
-----

This app owns its own cron daemon, launch it with: ::

  ./manage.py crond

The daemon will act as a classic cron and will run each task in a new thread,
leaving the main one continuing.

From admin
~~~~~~~~~

The cron table is set in database and the Django admin site is a quick
solution to manage you jobs.

From Python
~~~~~~~~~~

Just play with the model: ::

  from dbcron.models import Job

  # Run now() each minute
  job = Job.object.create(
      name='My job',
      func='django.utils.timezone.now',
      is_active=True,
      sec="0",
      min="*/1,
      hou="*",
      dom="*",
      mon="*",
      dow="*",
      yea="*"
  )

  # Test it
  job.run()

Warning
-------

The cron daemon launches jobs as they are requested with:

- function's path
- arguments and keyword arguments

There's no security about who/when/how, just functions launched abritairly,
Be careful who can set crontab, and do not hesitate to limit possible values.
