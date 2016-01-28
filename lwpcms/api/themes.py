import glob
import os
import json
import ntpath


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

def render_stylesheet(name):
    theme = get_activated_theme()
        
    if theme is not None:
        css_path = '{}/static/css/'.format(theme['path'])

        stylesheets = []

                                                                        
        for file in list(glob.glob('{}/*.css'.format(css_path))):
            if ntpath.basename(file) != name:
                continue

            reader = open(file)
            style = reader.read()
            reader.close()
            
            return '<style>' + style + '</style>'
