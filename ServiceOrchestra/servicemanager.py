from typing import Dict, Any
import subprocess

class ServiceManager:
    def __init__(self):
        pass

    def execute(self, op, service):
        return subprocess.run(['systemctl', op, service], stdout=subprocess.PIPE)


    def status(self, name) -> Dict[str, Any]:
        service_status = {
            'name': name,
            'enabled': False,
            'running': False,
        }
        result = self.execute('status', name).stdout
        if result.find(b"; enabled;") != -1:
            service_status['enabled'] = True
        if result.find(b"Active: active (running)") != -1:
            service_status['running'] = True

        return service_status
