CELERY_VHOST = '/'
ALEXA_AUTH = 'secretsecretsecret'
MERCURY_HOST = '192.168.1.1'
MERCURY_PORT = 5000

try:
    from local_settings import *
except:
    pass
