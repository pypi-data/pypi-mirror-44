===========
CommonStuff
===========

CommonStuff is a Django reusable app, what holds templatetags, management
commands, admin filters, middlewares, abstract models, etc. used in most of
my Django projects.

Think of it as a custom django-annoying. This app is in public mainly because
it is a dependency of another reusable app.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. `pip install django_commonstuff`
   
2. Add "commonstuff" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        'django.contrib.sites',  # optional, but usefull to commonstuff app
        # ...
        'commonstuff',
    )

3. Configure django_commonstuff in settings.py (see docs/SETTINGS.txt).

4. Run `python manage.py migrate` to create models.
