# LWPCMS
> ##### (L)ight(w)eight (P)ython (C)ontent (Ma)nagement (S)ystem
> ([See full documentation here](http://docs.lwpcms.com/))
> LWPCMS is a web content management system written in python.
> Most people would probably compare it with Wordpress.

> LWPCMS is currently in the alpha stage, work-in-progress.
> A demo will be out once it reaches the beta stage; alhough, you are
free to use it right now or why not contribute to the project?

> ##### LWPCMS will bring you:
> * Management of content.
> * File/Attachment uploading.
> * User management.
> * Website traffic analytics.
> * Module/Plugins. (plugins are called modules in LWPCMS, since they are
100% structured like python module/packages.)
> * Hooks. ([See available hooks](lwpcms/api/constants.py))
> * Themes.
> * Full access to source code.

> Some of these stuff are not implemented yet, please see "issues".<br>
> And of course, there is more to come...<br>
> <b><i>
Contribute to the project by implementing the "TODO" stuff on "issues"!</i></b>
<br>

> ##### Standards
> If you're using LWPCMS, you should follow these standars/recommendations:
> * Just because you are allowed to edit the source code does not mean you
should (unless you are contributing). If there is an LWPCMS update, it will
probably break your site if you have edited the source code.
> * Instead of editing the source code, create a module/plugin for your needs.

## How to set up the dev environment
> * clone, pull down the repo.
> * cd into the folder.
> * cd into lwpcms/static.
> * Run:

        mkdir upload

> * cd back to the root of the project.
> * Run:

        python3 __main__.py

> * Open up another shell.
> * cd into lwpcms/static/css
> * Run:

        sass --watch style.scss style.css

> * (You will need to install sass for this)
> * You're good to go!, start contributing to the project :)
