from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# This avoids the frustrating step of having to set up a new admin
# user every time you re-initialize your database.
# http://schbank.wordpress.com/2011/12/04/django-automatically-create-an-admin-user-during-syncdb/
# https://djangosnippets.org/snippets/1875/

from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.contrib.auth import models as auth_models
from django.conf import settings

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)

def create_admin(app, created_models, verbosity, **kwargs):
    if settings.DEBUG:
        try:
            auth_models.User.objects.get(username='admin')
        except auth_models.User.DoesNotExist:
            print '*' * 80
            print 'Creating admin user -- login: admin, password: admin'
            print '*' * 80
            assert auth_models.User.objects.create_superuser('admin', 'admin@domain.com', 'admin')
    else:
        print 'Admin user "admin" already exists.'

signals.post_syncdb.connect(
    create_admin,
    sender=auth_models,
    dispatch_uid='apps.auth.models.create_admin'
)
