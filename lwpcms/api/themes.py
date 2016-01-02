import glob
import os
import json


def get_activated_theme():
    avail_themes = glob.glob('lwpcms/themes/*_theme')
    for avail_theme in avail_themes:
        with open('{}/theme.json'.format(avail_theme)) as file:
            data = json.loads(file.read())
            theme = data['theme']
            theme['path'] = avail_theme
            
            if 'activated' in theme:
                if theme['activated']:
                    return theme

    return None