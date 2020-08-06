import logging
import json
import aiohttp_jinja2
import jinja2
import config
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from servicemanager import ServiceManager
from routes import init_routes

class RunningEnabledTestCase(AioHTTPTestCase):

    async def get_application(self):

        app = web.Application()
        app['logging'] = logging.getLogger('dummy')
        app['service'] = {'name':'dummy.service', 'controllable': True}

        def execute(self, op=None, s=None):
            pass

        def status(self, n=None):
            return {
                'name': self or n,
                'enabled': True,
                'running': True,
            }

        app['service_manager'] = ServiceManager()
        app['service_manager'].execute = execute
        app['service_manager'].status = status

        aiohttp_jinja2.setup(app,
                             loader=jinja2.FileSystemLoader(str(config.BASE_DIR / 'ServiceOrchestra' / 'templates')))
        init_routes(app)
        return app


    @unittest_run_loop
    async def test_disable(self):
        resp = await self.client.request("GET", "/disable")
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert result['success'] == False


    @unittest_run_loop
    async def test_stop(self):
        resp = await self.client.request("GET", "/stop")
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert result['success'] == False


    @unittest_run_loop
    async def test_start(self):
        resp = await self.client.request("GET", "/start")
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert result['success'] == True
        assert len(result['result']) > 0
        assert result['result'][0]['name'] == 'dummy.service'
        assert result['result'][0]['controllable'] == True

    async def test_enable(self):
        resp = await self.client.request("GET", "/enable")
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert result['success'] == True
        assert len(result['result']) > 0
        assert result['result'][0]['name'] == 'dummy.service'
        assert result['result'][0]['controllable'] == True

    async def test_restart(self):
        resp = await self.client.request("GET", "/restart")
        assert resp.status == 200
        text = await resp.text()
        result = json.loads(text)
        assert result['success'] == True
        assert len(result['result']) > 0
        assert result['result'][0]['name'] == 'dummy.service'
        assert result['result'][0]['controllable'] == True


if __name__ == '__main__':
    pass
    #unittest.main()
