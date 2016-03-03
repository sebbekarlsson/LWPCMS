import glob
import os
import json
import ntpath
import base64
import urllib.request
import tarfile


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



def install_theme(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    fname = os.path.basename(url)
    fname_path = 'lwpcms/themes/{}'.format(fname)

    with open(fname_path, 'wb') as the_file:
        the_file.write(data)

    tar = tarfile.open(fname_path, "r:gz")
    tar.extractall(path='lwpcms/themes/.')
    tar.close()

    for fl in glob.glob('lwpcms/themes/*.tar'):
        os.remove(fl)

    return True
