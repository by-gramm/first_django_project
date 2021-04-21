import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings.prod')

application = get_wsgi_application()

project_folder = os.path.expanduser('C:/Dev/first_project/')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))
