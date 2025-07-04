"""
WSGI config for shoppingList project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
import os
from dotenv import load_dotenv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppingList.settings')

project_folder = os.path.expanduser('~/lucirion-shopping-list-app')
load_dotenv(os.path.join(project_folder, '.env'))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
