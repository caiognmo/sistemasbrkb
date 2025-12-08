import os
import sys

# Caminho para a pasta do seu projeto
path = '/home/caiogab/SistemasBr-KB'
if path not in sys.path:
    sys.path.insert(0, path)

# Ativa o ambiente virtual
activate_this = '/home/caiogab/.virtualenvs/SistemasBr-KB-virtualenv/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

# Configura o Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
