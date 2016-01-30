import json
import os
import argparse


config_name = 'config.json'
parser = argparse.ArgumentParser()

parser.add_argument('--database_name')
parser.add_argument('--set_demo')
parser.add_argument('--run')
args = parser.parse_args()

if os.path.isfile(config_name):
    file = open(config_name, 'r')
    config = json.loads(file.read())
    file.close()

    print('{} already exists, remove to reset.'.format(config_name))
else:
    
    if args.database_name:
        database_name = args.database_name
    else:
        database_name = input('Choose database name: ')

    data = {
            'database_name': database_name
           }

    if args.set_demo:
        data['demo'] = True

    print(data)
    print('Finished installing.')

    with open(config_name, 'w+') as file:
        file.write(json.dumps(data))


if args.run:
    from lwpcms.app import app
    app.run(debug=True)