from aiohttp import web
import logging
import logging.handlers
import config

from config import log
from routes import init_routes, init_static_routes
from servicemanager import ServiceManager
import aiohttp_jinja2
import jinja2
import json


def init_logger():
    my_logger = logging.getLogger(log['tag'])
    my_logger.setLevel(log['level'])

    handler = logging.handlers.SysLogHandler(address=log['address'])

    my_logger.addHandler(handler)
    return my_logger

def init_app():
    app = web.Application()
    app["logging"] = init_logger()
    app['service_manager'] = ServiceManager()
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(str(config.BASE_DIR / 'ServiceOrchestra' / 'templates')))

    init_routes(app)
    init_static_routes(app)

    return app

async def on_startup(app):
    with open(config.service_file, 'r') as f:
        app['service'] = json.loads(f.read())


async def on_shutdown(app):
    with open(config.service_file, 'w') as f:
        f.write(json.dumps(app['service']))

if __name__ == '__main__':
    app = init_app()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app)
