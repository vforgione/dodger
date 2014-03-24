import newrelic.agent
newrelic.agent.initialize('/home/deploy/dodger-env/dodger/config/newrelic.ini')

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dodger.settings.prod")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
