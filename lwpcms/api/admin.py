import json
from lwpcms.api.modules import call_module_event
from lwpcms.api.constants import hooks


def get_sidenav():
    """ Return Object
    This function is used to get the admin-side-navigator.
    It also calls every activated module so that they can use the navigator before
    it gets rendered.
    """
    with open('lwpcms/static/shards/admin/side_nav.json') as file:
            nav = json.loads(file.read())

            call_module_event(hooks['admin_sidenav'], {'nav': nav})

            return nav
