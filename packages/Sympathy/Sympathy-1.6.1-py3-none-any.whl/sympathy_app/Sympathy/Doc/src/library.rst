.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2010-2019 System Engineering Software Society
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

.. _`libraries`:

Libraries
=========

.. _`library_wizard`:

Creating new libraries
----------------------
When Sympathy starts it looks for nodes in all folders in
*File->Preferences->Node Libraries* in Sympathy. So to create your own node or
plugins, first you have to create a library and add it to Sympathy's list of
libraries.

To create a library all you need to do is use the Library Wizard.
Start it by clicking *File->Wizards->New Library*.

On the first page you will add some meta data about your library. Only name
and identifier are mandatory, but go ahead and add as much as you can!

On the second page you will select the path where the library will be saved,
and a preview of the folders and files created will be displayed.
You can change the common package name if you want, but this is not needed.

When you have finished the wizard, the library has been automatically added to
*File->Preferences->Node Libraries*. Note, this is not synonymous with adding
libraries to the library view.


.. _`library_metadata`:

Library meta data
-----------------
The file Library.ini in the library root may contain extra meta data for the
library. The following fields are recognized in the General section:

``name``
  The human readable name of the library.

``description``
  The human readable description of the library.

``identifier``
  And identifier for this library. Should only contain 

``library_path``
  The path of the library folder relative to the library root.

``common_path``
  The path of the package inside the common folder relative to the library root.

``maintainer``
  The name and contact information of the current maintainer of the libary.
  Can be an indiviual person, an organisation or a community.

``copyright``
  A copyright notice that is shown with all nodes.

``repository``
  Url to repository for the library).


.. _`library_structure`:

Library structure
-----------------
This is the recommended way to structure a node library::

  <Library root>
  ├─ Library
  │  └─ <Library name>
  │     └─ ... (nodes & plugins)
  ├─ Common
  │  └─ <package_name>
  │     └─ ... (python modules)
  ├─ Tests
  │  ├─ Unit
  │  └─ Workflow
  ├─ Examples
  └─ library.ini

The Library folder is where you put nodes and plugins. The Common folder is for
additional python modules. Tests of your library's functionality should be
placed in Tests and Example flows that show off how your nodes work should be
placed in Examples. Tests and Exampels folders are completely optional.


Add extra modules to your library
---------------------------------
If your node code is starting to become too big to keep it all in a single file
or if you created some nice utility functions that you want to use in several
different node files you can place them in the common python package. I.e. the
subfolder to the folder *Common*.

..
   Now you can add modules to the package by adding the python files to the folder::

       > spyder boblib/Common/boblib/mymodule.py

Open your favorite editor and create the file::

    boblib/Common/boblib/mymodule.py

The *Common* folder will automatically be added to ``sys.path`` so you will now
be able to import modules from that package in your node code::

    from boblib import mymodule


.. _`library_tags`:

Library tags
------------
Each library may define additional node tags. These tag definitions go into the
file Common/<package_name>/__init__.py, and it can look something like this::

    from sympathy.api.nodeconfig import LibraryTags, TagType, GroupTagType


    def library_tags():
        return [
            ExamplelibLibraryTags
        ]


    class ExamplelibLibraryTags(LibraryTags):
        class_tags = (
            GroupTagType(
                'example',

                # First group
                [GroupTagType(
                    'GroupOne',
                    [TagType('TagOne',
                             'Tag description'),
                     TagType('TagTwo',
                             'Tag description')]
                ),

                # Second group
                GroupTagType(
                    'GroupTwo',
                    [TagType('TagOne',
                             'Tag description',
                             name='Optional tag name that can hold non-alphabetic characters')]
                ),

                # Third group
                GroupTagType(
                    'GroupThree',
                    [TagType('TagOne',
                             'Tag description'),
                     TagType('TagTwo',
                             'Tag description'),
                     TagType('TagThree',
                             'Tag description')],
                    name='Optional group name that can hold non-alphabetic characters')
                ]
            )
        )

        def __init__(self):
            super().__init__()
            self._root = self.class_tags

This will create a structure like below (if using Separated Tag Layout,
otherwise the tags will be mixed in with those already existing):

.. figure:: screenshot_example_tags.png
   :scale: 50%
   :alt: Custom tags example
   :align: center

Note that tags won't show up in the tree until they are used by at least one
node.


.. _example_flows:

Example flows
-------------
Workflows in the Examples directory (create it, if it does not exist, before
adding example flows) of a library will be treated as examples.

Example flows are treated similarly to test workflows in that they are executed
automatically when running the built-in test suite. See :ref:`lib_tests`.

Additionally, example flows can specify (on the top-level) that they are
examples for one or several nodes by including a reference in the following
format: :code:`Node example: *<node-identifier>*` (for example, :code:`Node
example: *com.example.boblib.helloworld*`) inside text fields.  Alternatively,
to make the example reference fit better as part of a sentence, the following
format is also supported: :code:`Node example for *<node-identifier>*`.

The documentation for referenced nodes will include links to referencing
example flows. Example flows are copied into the documentation folder and as a
rule, it is best if they are self-contained and do not depend on other
workflows or data files.
