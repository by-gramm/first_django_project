import os
import sys

from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings.prod')

project_folder = os.path.expanduser('C:/Dev/first_project/')  # adjust as appropriate
# load_dotenv(os.path.join(project_folder, '.env'))

# path = '/home/bygramm/first_django_project'
# if path not in sys.path:
#     sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'first_project.settings.prod'

application = StaticFilesHandler(get_wsgi_application())
