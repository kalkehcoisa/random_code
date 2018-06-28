import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/kalkehcoisa/webapps/mosca_app/mosca/mosca/")
sys.path.insert(1, "/home/kalkehcoisa/webapps/mosca_app/mosca/mosca/mosca/")
sys.path.insert(2, "/home/jayme/projetos/mosca/mosca/mosca/")

from runserver import application
application.secret_key = 'Add your secret key'
