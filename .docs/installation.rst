- Before You start, its highly recommended to update pip and setup tools:


.. code-block:: bash

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools


.. include:: ./installation_via_pypi.rst

- to install the latest version from github via pip:


.. code-block:: bash

    python -m pip install --upgrade git+https://github.com/bitranox/lib_travis.git


- include it into Your requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_travis

    # for the latest development version :
    lib_travis @ git+https://github.com/bitranox/lib_travis.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version from source code:

.. code-block:: bash

    # cd ~
    $ git clone https://github.com/bitranox/lib_travis.git
    $ cd lib_travis
    python setup.py install


.. include:: ./installation_via_makefile.rst
