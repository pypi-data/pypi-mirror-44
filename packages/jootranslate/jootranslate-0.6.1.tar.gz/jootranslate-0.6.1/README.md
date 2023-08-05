[![](https://img.shields.io/pypi/v/jootranslate.svg)](https://pypi.python.org/pypi?name=jootranslate&:action=display)  [![](https://travis-ci.org/pfitzer/jtranslate.svg?branch=master)](https://travis-ci.org/pfitzer/jtranslate) [![](https://pyup.io/repos/github/pfitzer/jtranslate/shield.svg?t=1520427395490)](https://pyup.io/account/repos/github/pfitzer/jtranslate/) ![](https://pyup.io/repos/github/pfitzer/jtranslate/python-3-shield.svg?t=1520427395491)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jootranslate.svg)](https://pypi.python.org/pypi?name=jootranslate&:action=display)


## jootranslate
Searches for JText::_ translations in php files and generates the ini files. If the file exist only new translation strings will
be added.

This is just a little helper so you don`t have to copy and paste all your translation strings by hand.

Your component needs the following directory structure

    administrator
        - components
            - com_COMPONENTNAME
                - controllers
                - language
                - etc ...
    components
        - com_COMPONENTNAME
            - controllers
            - language
            - etc...

**installation**

use pip

    pip install jootranslate

local

    python setup.py install

**usage**


    jootranslate --source /path/to/component/root --com your_component

to see a full list of all options

    jootranslate -h

**todo**

Parse the xml files for translations and generate the *.sys.ini files