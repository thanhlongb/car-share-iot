.. Car Share IoT documentation master file, created by
   sphinx-quickstart on Mon Sep 21 16:36:47 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Car Share IoT's documentation!
=========================================
'Car Share IoT' is our project for final assignment of Programming IoT Course. It is a automatic car share system with a web application which allow user to rent a car through the website, report the car status, lock and unlock the car using traditional password, facial recognition or bluetooth. The web application is also a platform to manage and track the car rental history, car status and basic analytics for manager. 

Getting Started
----------------

Installation
++++++++++++

First go to the ``masterpi`` folder to install project dependencies in requirements.text

.. code-block:: bash

   pip3 install -r requirements.txt

To run the web application in the master pi, run the ``run.py`` file

.. code-block:: bash

   python3 run.py

To run the application for lock and unlock the car in agent pi, moved to ``agent pi`` directory and run the ``main.py``

.. code-block:: bash

   python3 main.py


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Users API
---------

Models
++++++
.. autoclass:: app.users.usersModels
    :members:
    :undoc-members:


Views
+++++
.. autoclass:: app.users.usersViews
    :members:
    :undoc-members:


REST APIs
+++++++++
.. autoclass:: app.users.UsersAPI
    :members:
    :undoc-members:


Cars API
--------

Models
++++++
.. autoclass:: app.cars.models
    :members:
    :undoc-members:


Views
+++++
.. autoclass:: app.cars.views
    :members:
    :undoc-members:


REST APIs
+++++++++
.. autoclass:: app.cars.api
    :members:
    :undoc-members:

Bookings API
------------

Models
++++++
.. autoclass:: app.bookings.models
    :members:
    :undoc-members:


Views
+++++
.. autoclass:: app.bookings.views
    :members:
    :undoc-members:


REST APIs
+++++++++
.. autoclass:: app.bookings.api
    :members:
    :undoc-members:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
