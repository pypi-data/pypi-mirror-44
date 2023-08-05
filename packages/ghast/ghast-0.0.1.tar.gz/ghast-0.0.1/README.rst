#####
ghast
#####

.. image:: https://travis-ci.com/nklapste/ghast.svg?token=PXHp9tdymHUxZDzfWpfK&branch=master
    :target: https://travis-ci.com/nklapste/ghast
    :alt: Build Status

Graylog HTTP Alert Script Triggerer (ghast)!

A simple server for triggering a script on a Graylog HTTP alert callback!

Requirements
============

* Python 3.5+

Installation
============

ghast can be installed via pip:

.. code-block:: bash

    pip install ghast

Example Usage
=============

To start and enable ghast to trigger the script ``./foo.sh`` when a
Graylog HTTP alert callback is sent to the url ``http://localhost:8000/bar``
run the following command:

.. code-block:: bash

    ghast --alert-url /bar --alert-script ./foo.sh

To get additional usage help on ghast run the following console command:

.. code-block:: bash

    ghast --help
