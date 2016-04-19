import os
import glob
import json
import importlib


def get_modules():
    """ Return a list
    This function is used to get all available modules.
    """
    modules = []

    avail_modules = glob.glob('lwpcms/modules/*_module')
    for avail_module in avail_modules:
        with open('{}/module.json'.format(avail_module)) as file:
            data = json.loads(file.read())
            module = data['module']
            module['path'] = avail_module
            
            modules.append(module)

    return modules


def get_activated_modules():
    """ Return a list
    This function is used to get all activated modules.
    """
    modules = []

    avail_modules = glob.glob('lwpcms/modules/*_module')
    for avail_module in avail_modules:
        with open('{}/module.json'.format(avail_module)) as file:
            data = json.loads(file.read())
            module = data['module']
            module['path'] = avail_module
            
            if 'activated' in module:
                if module['activated']:
                    modules.append(module)

    return modules


def call_module_event(event, data):
    """ Return Object || Dict || List || String || ?
    This function is used to call an event on all modules.
    The module can later use this event.
    """
    modules = get_activated_modules()
    results = []

    for module in modules:
        obj = importlib.import_module(
                module['path'].replace('/', '.') + '.module')
        
        result = obj.module.event(event, data)

        if result is not None:
            results.append(result)

    return results
