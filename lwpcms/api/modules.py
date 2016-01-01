import os
import glob
import json
import importlib


def get_activated_modules():
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
    modules = get_activated_modules()
    results = []

    for module in modules:
        obj = importlib.import_module(
                module['path'].replace('/', '.') + '.module')

        results.append(obj.module.event(event, data))

    return results
