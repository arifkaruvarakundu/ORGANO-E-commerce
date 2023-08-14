"""
WSGI config for organo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

<<<<<<< HEAD
# organo/wsgi.py

=======
>>>>>>> 01a0301d8dfcd546fea09e3e44adb69ca2c3a6d0
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organo.settings')

<<<<<<< HEAD
application = get_wsgi_application()
=======
application = get_wsgi_application()
>>>>>>> 01a0301d8dfcd546fea09e3e44adb69ca2c3a6d0
