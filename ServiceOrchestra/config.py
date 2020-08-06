import logging
import pathlib

log = {
    'tag': 'ServiceOrchestra',
    'address': '/dev/log',
    'level' : logging.DEBUG
}

service_file = 'controllable_services.json'

BASE_DIR = pathlib.Path(__file__).parent.parent