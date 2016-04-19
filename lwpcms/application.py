"""
This piece of code is mainly for parsing the configuration.
"""
import argparse
import configparser
import os


# READ ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('--config')
args = parser.parse_args()

# MAKE SURE WE GET THE CONFIGURATION FILE
if args.config is None or args.config == '':
    exit('--config <path>')

if not os.path.isfile(args.config):
    exit('COULD NOT FIND CONFIGURATION FILE')

# READ THE  CONFIGURATION FILE
config = configparser.ConfigParser()
config.read(args.config)
