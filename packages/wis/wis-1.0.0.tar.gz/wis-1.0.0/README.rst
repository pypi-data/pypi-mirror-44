==================
MPC wis.py Project
==================


.. image:: https://img.shields.io/pypi/v/wis.svg
        :target: https://pypi.python.org/pypi/wis

.. image:: https://img.shields.io/travis/matthewjohnpayne/wis.svg
        :target: https://travis-ci.org/matthewjohnpayne/wis

.. image:: https://readthedocs.org/projects/wis/badge/?version=latest
        :target: https://wis.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


wis.py tells you the position of a satellite (e.g. in heliocentric coordinates).

wis.py uses JPL spice kernels, so you need spicypy.

wis.py goes and gets the spice-kernels if you don't have them.

    
wis.py is essentially a means to automate the retrieval of
useful spice-kernels. 
All of the positional calculations are handled using spice/spiceypy.

wis.py does *not* know about *all* satellites.

So far it only knows about:
* TESS
* K2
* CASSINI
 
wis.py is very light & wispy ...

wis 
* ~ Where Is Satellite
* ~ Where Is Satellite-spice-kernel


* Free software: MIT license
* Documentation: https://wis.readthedocs.io. or  or https://mpcutilities.readthedocs.io. ??? 


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
