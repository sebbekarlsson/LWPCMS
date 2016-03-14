import json
from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks


def get_sidenav():
    with open('./lwpcms/static/shards/admin/side_nav.json') as file:
            nav = json.loads(file.read())

            call_module_event(hooks['admin_sidenav'], {'nav': nav})

            return nav
