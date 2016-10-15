


Deep Q Learn
============


Getting Started
---------------

.. code :: sh

    # MacOS
    cd deepqpong
    sudo easy_install pip
    sudo pip install --upgrade virtualenv
    virtualenv venv
    source venv/bin/activate
    
    # linux(Ubuntu):  
    cd deepqpong
    sudo apt-get install --upgrade python-pip
    sudo pip install --upgrade virtualenv
    virtualenv venv
    source venv/bin/activate

Install ``tensorflow``


    pip install --upgrade https://storage.googleapis.com/tensorflow/mac/tensorflow-0.7.1-cp27-none-any.whl


.. code :: sh

    $ python


.. code :: python

    >>> import tensorflow as tf


Install ``pygame``

.. code :: sh

    pip install pygame


Clone PyGamePlayer

.. code :: sh

    mkdir deepqpong
    cd deepqpong

    # clone PyGamePlayer
    git clone https://github.com/DanielSlater/PyGamePlayer
    mv PyGamePlayer pygame_player


I could not import ``cv2`` package, had to install ``opencv``

a few references

`<http://www.mobileway.net/2015/02/14/install-opencv-for-python-on-mac-os-x/>`_


.. code :: sh

    brew install opencv

check version of opencv

::

    $ls /usr/local/Cellar/opencv

    2.4.13_3


use the version number to get the path, and verify opencv installation
next command should display ``cv.py`` and `` cv2.py``

::

    $ls /usr/local/Cellar/opencv/2.4.13_3/lib/python2.7/site-packages/

    cv.py	cv2.so


Next, from project root dir, execute (use appropriate opencv version)

::

    cp /usr/local/Cellar/opencv/2.4.13_3/lib/python2.7/site-packages/cv* ./venv/lib/python2.7/site-packages




Installation
------------

To install package ``deepqlearn``, ``cd`` into project-dir and run

.. code:: bash

    pip install .

or, (recommended for dev) use following command if modifications to code
should be immediately available

.. code:: bash

    pip install -e .

To **update an existing installation**, ``cd`` into project-dir and run

.. code:: bash

    python setup.py develop




- Noes on ``setup.py``

    1) The ``setup.py`` script checks for requirements in ``./requirements.txt``
    (included in the package) and tries to install/upgrade dependencies.

    2) The default entry point is set to:
    ``'console_scripts': ['deepqlearn=']``
    which calls the risk scoring pipeline





Dev/Test
--------

To run code in the ``__main__`` block of each module,
from any working dir, run


.. code:: bash

    python -m deepqlearn.<modulename>

e.g.

.. code:: bash

    python -m deepqlearn.preprocess

``-m`` is required since module belongs to a package, and
also note the missing ``.py`` extension after the module name


Other way to run the code in ``__main__`` block is to
``cd`` in to the ``deepqlearn/`` dir and run

.. code:: bash

    python <modulename>.py

Note the ``.py`` extension in this case.


Experimental test cases can be found in ``deepqlearn/tests/``. To
run these test cases, ``cd`` in to project dir and use

.. code:: bash

    python setup.py test
