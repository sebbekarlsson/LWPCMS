import glob
import os
import json
import ntpath
import base64


def get_themes(name=None):
    avail_themes = glob.glob('lwpcms/themes/*_theme')
    
    themes = []

    for avail_theme in avail_themes:
        with open('{}/theme.json'.format(avail_theme)) as file:
            data = json.loads(file.read())
            theme = data['theme']
            theme['path'] = avail_theme.replace('lwpcms/', '')
            themes.append(theme)

            if name is not None:
                if theme['name'] == name:
                    return theme

    return themes


def get_activated_theme():
    avail_themes = glob.glob('lwpcms/themes/*_theme')
    for avail_theme in avail_themes:
        with open('{}/theme.json'.format(avail_theme)) as file:
            data = json.loads(file.read())
            theme = data['theme']
            theme['path'] = avail_theme.replace('lwpcms/', '')
            
            if 'activated' in theme:
                if theme['activated']:
                    return theme

    return None
