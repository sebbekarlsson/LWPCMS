from lwpcms.config import config
from lwpcms.api.posts import get_option


def is_site_demo():
    return get_option('site_demo')['value']
