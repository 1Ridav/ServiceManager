from api import api
from views import views


def init_routes(app):
    app.router.add_route('GET', '/', views.index, name='index')

    app.router.add_route('GET', '/status', api.status, name='status')
    app.router.add_route('POST','/status', api.status_post, name='status_post')
    app.router.add_route('GET', '/enable', api.enable, name='enable')
    app.router.add_route('GET', '/disable', api.disable, name='disable')
    app.router.add_route('GET', '/start', api.start, name='start')
    app.router.add_route('GET', '/stop', api.stop, name='stop')
    app.router.add_route('GET', '/restart', api.restart, name='restart')

def init_static_routes(app):
    app.router.add_static('/static/js/', path='static/js/', name='static', follow_symlinks=True)

