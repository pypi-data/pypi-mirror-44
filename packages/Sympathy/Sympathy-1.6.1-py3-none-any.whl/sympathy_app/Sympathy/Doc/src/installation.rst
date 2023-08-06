.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2017-2019 System Engineering Software Society
..
..     Sympathy for Data is free software: you can redistribute it and/or modify
..     it under the terms of the GNU General Public License as published by
..     the Free Software Foundation, either version 3 of the License, or
..     (at your option) any later version.
..
..     Sympathy for Data is distributed in the hope that it will be useful,
..     but WITHOUT ANY WARRANTY; without even the implied warranty of
..     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
..     GNU General Public License for more details.
..     You should have received a copy of the GNU General Public License
..     along with Sympathy for Data. If not, see <http://www.gnu.org/licenses/>.

.. _installation:

Installation instructions
=========================


Using installer
---------------

If you are using Windows we offer a pre-built executable installer which
contains everything needed to run Sympathy.

Download the latest version of Sympathy from the `official homepage
<https://www.sympathyfordata.com/>`_.

After downloading, run the installer and follow the instructions. This will
install Sympathy. Once done, you can start Sympathy from the start menu.


Manual install
--------------

If you do not run Windows or prefer to install Sympathy manually instead of
using our installer there are a few steps required.

First install or choose an existing python environment.  Then optionally, but
highly recommended, create a virtual python environment.  Finally install
Sympathy into that environment.


Install Python base environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optional if you already have a suitable installation of Python 3.6+ with pip
installed.

Windows
#######

On Windows, you have to download and install an appropriate version of `Python
<https://www.python.org/downloads/>`__. That is, Python 3.6 or later for amd64
architecture (64 bit Windows). Choose executable or web based installer and make
sure to include pip while installing.


Mac OS
######

These instructions are written for MacOS X 10.13.3, using MacPorts.

Start by installing XCode from the App Store (that will download an XCode
installer, so this is a two-stage process).

.. code-block:: bash

   sudo xcode-select --install
   sudo xcodebuild -license


Download and install `MacPorts <http://www.macports.org>`__.  Before continuing,
it is recommended update the package definitions.

.. code-block:: bash

   sudo port selfupdate

Then install the dependencies.

.. code-block:: bash

   sudo port install python36 unixODBC


Linux
#####
   
These installation instructions have been written for Ubuntu 16.04 which is the
only officially supported Linux distribution for Sympathy for Data.

First update your package definitions and update outdated packages.

.. code-block:: bash

   sudo apt-get update
   sudo apt-get dist-upgrade


Then install the required prerequisites

.. code-block:: bash

   sudo apt-get install build-essential python3-dev python3-venv unixodbc-dev


Create virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~

Optional if you already have a suitable installation of Python 3.6+ with
pip installed.  However, we strongly recommend that you use a virtual
environment rather than installing in a system level python installation.

Now, navigate to a directory in which you want to create the virtual
environment. In the following instructions, replace <python> with the path to
the python executable from the previous step. Also, replace <env-sympathy> with
the name that you want to use for the virtual environment.


Windows
#######

.. code-block:: bat

    <python> -m venv <env-sympathy>
    cd <env-sympathy>\Scripts
    activate.bat
    pip install -U pip setuptools wheel


Mac OS & Linux
##############


.. code-block:: bash

    <python> -m venv <env-sympathy>
    source <env-sympathy>/bin/activate
    pip install -U pip setuptools wheel


Install Sympathy from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~

With the desired python environment active, run the following to install
Sympathy. Replace <version> with the version that you would like to install or
omit ==<version> completely to install the latest version.

.. code-block:: bash

    pip install Sympathy==<version>
    python -m sympathy_app install

Now we are ready to run Sympathy!


Running Sympathy
~~~~~~~~~~~~~~~~

In order to run Sympathy using python, first make sure that the virtual
environment used in the installation steps is active. You can run Sympathy
either with a GUI (first command below), or for data processing applications in
head-less mode (second command). For a more comprehensive list of commands and
options, see :ref:`launch_options`.

.. code-block:: bash

  python -m sympathy_app gui
  python -m sympathy_app cli <my-workflow>

Installing the wheel also creates additional executables for your virtual
environment. These are typically located in folder called Scripts, on Windows,
and bin, on Unix. These run sympathy in the same way as above but does not
require the virtual environment to be activated beforehand.

.. code-block:: bash

  sympathy-gui
  sympathy-cli <my-workflow>


Troubleshooting
~~~~~~~~~~~~~~~

If you see any text in red during the execution of pip, this would typically
mean that some library is missing in your system. See the section for your OS
below for instructions on how to install packages.


Mac OS & Linux
##############

For example, if you get an error while installing pyodbc, that typically means
you need to install a package named unixODBC. Use port to install missing
libraries.

Some small functionality (like drag and dropping flows to open them) depends on
pyobjc being installed as well, on Mac. This pip package adds a lot of
dependencies however, so it is left to the user to decide if this is wanted:

.. code-block:: bash

    pip install pyobjc  # optional

Linux
#####

For example, if you get an error while installing pyodbc, that typically means
you need to install a package named unixodbc-dev, or unixODBC-devel (the names
tend to vary across Linux distributions). Use apt or the package manager that is
preferred by your distribution to install missing libraries.
