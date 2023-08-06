.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2018 System Engineering Software Society
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

.. _`pluginwriting`:

Creating Plugins
================

The standard library has a few nodes (import nodes, export nodes and calculator
nodes) that make use of plugins.  Plugins can be added to third-party libraries
to extend the functionality of these nodes in some intended ways.

Plugins are installed by adding python files inside the Library folder of a
library (<some-library>/Library/<some-folder>). The filename for the plugin
should match :code:`plugin_*.py`. These python files needs to contain a class
which is a subclass of the plugin class specified by the node. Installed plugins
are then automatcally loaded and made ready for use in nodes.


Import node plugins
-------------------

The specific base classes used for implementing plugins for import nodes inherit
the following base:

.. autoclass:: sympathy.api.importers.IDataImporter
   :members:

It serves as a common point for standardization and documentation but should not
be subclassed directly. Instead subclass the base class specified by the node.

Example
########

This example will serve to illustrate the fundamentals of creating import
plugins with custom parameters and GUI.

To extend :ref:`org.sysess.sympathy.data.table.importtable` with support for a
json subformat of table-like structure, for example, the following::

    [{"a": 1, "b": 2, "c": 3},
     {"a": 4, "b": 5, "c": 6},
     {"a": 7, "b": 8, "c": 9}]

Create a new file called plugin_json_table_importer.py with the
following code::

    import os
    import json
    import numpy as np
    from sympathy.api import qt as qt_compat2
    from sympathy.api import importers
    QtWidgets = qt_compat.import_module('QtWidgets')

    class JsonTable(importers.TableDataImporterBase):
        IMPORTER_NAME = 'JSON-TABLE'

        def __init__(self, fq_infilename, parameters):
            super(JsonTable, self).__init__(fq_infilename, parameters)
            if parameters is not None:
                if 'set_name' not in self._parameters:
                    parameters.set_boolean('set_name', value=True,
                                           label='Set table name from filename')

        def valid_for_file(self):
            # Inefficient for large files, it would be better
            # to check some part of the content or perhaps even the file
            # extension. Additionally, this accepts all valid json files.
            try:
                with open(self._fq_infilename, 'rb') as f:
                    json.load(f)
                    return True
            except Exception:
                return False

        def import_data(self, out_table, parameters=None, progress=None):
            cols = {}
            with open(self._fq_infilename, 'rb') as f:
                for row in json.load(f):
                    for col_name, cell in row.items():
                        cols.setdefault(col_name, []).append(cell)
            for col_name, col_data in cols.items():
                out_table[col_name] = np.array(col_data)

            if parameters['set_name']:
                out_table.set_name(os.path.basename(self._fq_infilename))

        def parameter_view(self, parameters):
            # For importers without custom parameters, this need not
            # be implemented.
            if not self.valid_for_file():
                return QtGui.QWidget()
            return parameters['set_name'].gui()

Note that we are subclassing TableDataImporterBase which is the base class
for plugins specified in :ref:`org.sysess.sympathy.data.table.importtable`.

:ref:`Create a new library<library_wizard>` and move the file into
*Library/<Library name>/*

To try it out, create a new text file with data following the structure example
above, called table.json.

Configure :ref:`org.sysess.sympathy.data.table.importtable` to import using
*JSON-TABLE* and select table.json using the datasource node.

Now we have created a custom importer plugin for
:ref:`org.sysess.sympathy.data.table.importtable`. Plugins for
:ref:`org.sysess.sympathy.data.adaf.importadaf`,
:ref:`org.sysess.sympathy.data.text.importtext`, etc. should follow the same
structure and should be straight-forward to implement so long as you can handle
the source format (possibly by using a third-party library) and know the sympathy
datatype.


Export node plugins
-------------------

The specific base classes used for implementing plugins for export nodes inherit
the following base:

.. autoclass:: sympathy.api.exporters.IDataExporter
   :members:

It serves as a common point for standardization and documentation but should not
be subclassed directly. Instead subclass the base class specified by the node.


Calculator node plugins
-----------------------

All calculator nodes use the following base class for implementing plugins (it
can subclassed directly):

.. autoclass:: sylib.calculator.plugins.ICalcPlugin
   :members:

