import traceback
from aiohttp import web


async def enable(request):
    try:
        service = request.app['service']
        if not service['controllable']:
            raise NotControllableException

        service_manager = request.app['service_manager']

        service_manager.execute('enable', service['name'])
        service_manager.execute('start', service['name'])
        result = service_manager.status(service['name'])

        if result['enabled']:
            request.app['logging'].info(f"{service['name']} enabled")
            result.update({'controllable': request.app['service']['controllable']})
            response = {"success": True}
            response['result'] = [result]
        else:
            request.app['logging'].info(f"{service['name']} failed to enable")
            response = {"success": False}
        return web.json_response(response)
    except NotControllableException:
        return web.json_response({"success": False})
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.enable has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def disable(request):
    try:
        service = request.app['service']
        if not service['controllable']:
            raise NotControllableException

        service_manager = request.app['service_manager']

        service_manager.execute('stop', service['name'])
        service_manager.execute('disable', service['name'])
        result = service_manager.status(service['name'])

        if not result['enabled'] and not result['running']:
            request.app['logging'].info(f"{service['name']} disabled")
            result.update({'controllable': request.app['service']['controllable']})
            response = {"success": True}
            response['result'] = [result]
        else:
            request.app['logging'].info(f"{service['name']} failed to disable")
            response = {"success": False}
        return web.json_response(response)
    except NotControllableException:
        return web.json_response({"success": False})
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.disable has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def start(request):
    try:
        service = request.app['service']
        if not service['controllable']:
            raise NotControllableException

        service_manager = request.app['service_manager']

        service_manager.execute('start', service['name'])
        result = service_manager.status(service['name'])

        if result['running']:
            request.app['logging'].info(f"{service['name']} started")
            result.update({'controllable': request.app['service']['controllable']})
            response = {"success": True}
            response['result'] = [result]
        else:
            request.app['logging'].info(f"{service['name']} failed to start")
            response = {"success": False}
        return web.json_response(response)
    except NotControllableException:
        return web.json_response({"success": False})
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.start has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def stop(request):
    try:
        service = request.app['service']
        if not service['controllable']:
            raise NotControllableException

        service_manager = request.app['service_manager']

        service_manager.execute('stop', service['name'])
        result = service_manager.status(service['name'])

        if not result['running']:
            request.app['logging'].info(f"{service['name']} stopped")
            result.update({'controllable': request.app['service']['controllable']})
            response = {"success": True}
            response['result'] = [result]
        else:
            request.app['logging'].info(f"{service['name']} failed to stop")
            response = {"success": False}
        return web.json_response(response)
    except NotControllableException:
        return web.json_response({"success": False})
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.stop has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def restart(request):
    try:
        service = request.app['service']
        if not service['controllable']:
            raise NotControllableException

        service_manager = request.app['service_manager']

        service_manager.execute('restart', service['name'])
        result = service_manager.status(service['name'])

        if result['running']:
            request.app['logging'].info(f"{service['name']} restart succeded")
            response = {"success": True}
            result.update({'controllable': request.app['service']['controllable']})
            response['result'] = [result]
        else:
            request.app['logging'].info(f"{service['name']} failed to restart")
            response = {"success": False}
        return web.json_response(response)
    except NotControllableException:
        return web.json_response({"success": False})
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.restart has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def status(request):
    try:
        service = request.app['service']
        service_manager = request.app['service_manager']

        result = service_manager.status(service['name'])

        result.update({'controllable': service['controllable']})
        response = {"success": True}
        response["result"] = [result]

        return web.json_response(response)
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.status has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)


async def status_post(request):
    try:
        service = request.app['service']
        params = await request.json()

        service_manager = request.app['service_manager']
        result = service_manager.status(service['name'])

        service['controllable'] = params['controllable']

        response = {"success": True}
        result.update({'controllable': service['controllable']})
        response["result"] = [result]
        return web.json_response(response)
    except:
        traceback.print_exc()
        request.app['logging'].critical('api.status_post has thrown an exception ')
        response = {"success": False}
        return web.json_response(response)



class NotControllableException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None
        super().__init__(self.message)

    def __str__(self):
        return self.message