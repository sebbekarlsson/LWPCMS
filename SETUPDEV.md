# How to set up the dev environment

> * Make sure mongodb is running.
> * clone, pull down the repo.
> * cd into the folder.
> * Run:

        git submodule init
        git submodule sync
        git submodule update

> * cd into lwpcms/static.
> * Run:

        mkdir upload

> * cd back to the root of the project.
> * Create a configuration file wherever you want, in this format:

        [database]
        name = awesomename

> * Run:

        python3 setup.py develop
        python3 __main__.py --config myconfig.cfg

> * the "--config" argument needs to point to wherever your config file is.
> * Open up another shell.
> * cd into lwpcms/static/css
> * Run:

        sass --watch style.scss style.css

> * (You will need to install sass for this)

## Testing
> To run tests, cd into the root of the project and run:

        ./test.sh

> * You're good to go!, start contributing to the project :)
