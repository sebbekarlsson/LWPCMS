import os
import glob
import json
import importlib


def get_modules():
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

    print(event)

    for module in modules:
        obj = importlib.import_module(
                module['path'].replace('/', '.') + '.module')
        
        result = obj.module.event(event, data)

        if result is not None:
            results.append(result)

    return results
