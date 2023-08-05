pl-simpledsapp
==============

.. image:: https://badge.fury.io/py/simpledsapp.svg
    :target: https://badge.fury.io/py/simpledsapp

.. image:: https://travis-ci.org/FNNDSC/simpledsapp.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/simpledsapp

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-simpledsapp

.. contents:: Table of Contents


Abstract
--------

``simpledsapp`` is a simple DS plugin that copies directories file from an ``input`` to ``output``. If called with an optional ``--ignoreInputDir`` the plugin will simply write a JSON formatted timestamp to the output directory.

Synopsis
--------

.. code::

    python simpledsapp.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--prefix <filePrefixString>]                               \
        [--sleepLength <sleepLength>]                               \
        [--ignoreInputDir]                                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install simpledsapp

and run with

.. code:: bash

    simpledsapp.py --man /tmp /tmp

to get inline help. To copy from one directory to another, simply do

.. code:: bash

    simpledsapp.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-simpledsapp simpledsapp.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-simpledsapp simpledsapp.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------

Copy from input to output with a prefix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    mkdir in out && chmod 777 out
    docker run -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing       \
            fnndsc/pl-simpledsapp simpledsapp.py                    \
            --prefix test-                                          \
            --sleepLength 0                                         \
            /incoming /outgoing

The above will create a copy of each file in the container's ``/incoming`` and prefix the file copied with the ``prefix`` text (in this case "test-"). The copies will be stored in the container's ``/outgoing`` directory.

Simply write a timestamp to the output directory, ignoring the input completely
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    mkdir in out && chmod 777 out
    docker run -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing       \
            fnndsc/pl-simpledsapp simpledsapp.py                    \
            --ignoreInputDir                                        \
            /incoming /outgoing

This will simply create a file called ``timestamp.json`` in the output directory. This mode is useful to just create mock nodes in a Feed tree.



