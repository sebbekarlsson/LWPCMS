from lwpcms.api.posts import get_option
import random
import os


def is_site_demo():
    return get_option('site_demo')['value']


def get_random_greeting():
    greetings = [
            "Hope you're having a wonderful day!",
            "Nice to see you!",
            "The internet is amazing!",
            "Let's start working on your site!",
            "Nice to have you back!",
            "Welcome back!",
            "Let's publish something!"
            ]

    return greetings[random.randint(0, len(greetings)-1)]


def lwpcms_render_svg(filename):
    contents = ''
    abs_path = '{}{}'.\
    format(
            os.path.abspath(os.path.dirname(__file__)),
            '/../static/image/{}'.format(filename)
            )
    with open(abs_path, 'r+') as file:
        contents = file.read()

    file.close()

    return contents
