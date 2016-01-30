from lwpcms.config import config


def is_site_demo():
    if 'demo' not in config:
        return False
    else:
        return config['demo']
