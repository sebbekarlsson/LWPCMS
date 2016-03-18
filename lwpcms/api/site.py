from lwpcms.api.posts import get_option
import random


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
