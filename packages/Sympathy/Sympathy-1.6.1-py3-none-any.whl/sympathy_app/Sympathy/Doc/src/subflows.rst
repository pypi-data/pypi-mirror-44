.. This file is part of Sympathy for Data.
..
..  Copyright (c) 2010-2012 System Engineering Software Society
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

.. _subflows:

Subflows
--------
As your workflow grows it may start feeling a bit unwieldy after a while. To
improve the structure of the workflow you can create a subflows from some of
the nodes in your workflow. Select some nodes, right-click on one of them and
choose *Refactor->Create subflow from selection*. This will replace all the nodes that
you had selected with what looks like a single node, but is actually a subflow.
You can still get at the nodes by right-clicking on the subflow and choosing
*Edit*. This will open the "inside" of the subflow in a new tab. If you want to
get back to the flat workflow structure you can right-click on a subflow and
choose *Refactor->Expand subflow* to get all the nodes back where they were before.

.. figure:: screenshot_subflow_outside.png
   :alt: Example workflow
   :align: center

   Subflow outside. This workflow can be found in `<sympathy install
   directory>/Sympathy/Doc/workflows/ADAF example with subflow.syx`.

.. figure:: screenshot_subflow_inside.png
   :alt: Example workflow
   :align: center

   Subflow inside. This workflow can be found in `<sympathy install
   directory>/Sympathy/Doc/workflows/ADAF example with subflow.syx`.

Subflows can also contain yet other subflows so using this feature you can
structure your workflow hierarchically.


Adding ports
^^^^^^^^^^^^
Most of the time you want your subflow to take in data on some input ports and
produce output on some output ports. Each port symbol on the "outside" of the
subflow is also represented inside the subflow as a triangular node-like
element.

If you want to add a new input or output port simply right-click on an empty
area inside the subflow and choose *Ports->Input->Create* or *Ports->Output->Create*. A
corresponding port will appear on the outside of the subflow. You can connect
any data type to the little question mark of the port you just created.


.. _subflow_settings:

Subflow settings
^^^^^^^^^^^^^^^^

After you have created a subflow you can choose settings for how it should be
configured. Edit the subflow and, from its inside, Right-click on the subflow
and select *Settings* to launch a dialog for editing the current settings.

First of all choose the configuration dialogs that you want to include.
The setting is empty by default but you can add any of the configuration
dialogs from the nodes in the subflow. Move any nodes that you want from the
list of available nodes (left hand side) to the list of selected nodes (right
hand side).

You can use this to expose a portion of the configuration options for your
subflow, this is helpful to hide some of the underlying details. As an example,
starting out from the example workflow from :ref:`subflows` you might want to
expose only the configuration for a single node, such as: :ref:`Update ADAF with
Table` and hide everything else.

.. figure:: screenshot_subflow_settings.png
   :alt: Example subflow settings
   :align: center

   Subflow settings. This workflow can be found in `<sympathy install
   directory>/Sympathy/Doc/workflows/ADAF example with subflow.syx`.

There are two major modes to choose from: *Wizard configuration* and *Tab
configuration*. These determine how the configuration dialog will be
presented. By default *Tab configuration* is used. To change mode, simply check
or uncheck the checkbox labeled "Configure using wizard".

The checkbox labeled "Override parameters" is only used for linked subflows (see
:ref:`Linked Subflows`) and determine if changed parameters should be stored in
the subflow-link or in the workflow file that the subflow-link points to.


.. _subflow_config:

Subflow configuration
^^^^^^^^^^^^^^^^^^^^^

After you have created a subflow and edited its settings (See
:ref:`subflow_settings`) you can configure it by right-clicking on the
subflow and choosing *Configure*.

Depending on the mode, either a *Wizard configuration* dialog or a *Tab
configuration* dialog will appear.

To configure without considering the configuration mode from settings
right-click and choose *Advanced->Configure*, then choose the appropriate
configuration mode.


Tab configuration
#################

This configuration mode organizes the selected node dialogs in tabs. When
selected node dialogs include nested subflows their node dialogs will be grouped
together in a tab unless there is only one dialog.

Having all selected dialogs available as tabs provides a good overview and makes
it possible to quickly select the nodes of interest and configure them.

The tabs are ordered according to the order of selected nodes in
:ref:`subflow_settings`.

.. figure:: screenshot_subflow_tab_configuration.png
   :alt: Example subflow tab configuration
   :align: center

   Subflow tab configuration. This workflow can be found in `<sympathy install
   directory>/Sympathy/Doc/workflows/ADAF example with subflow.syx`.


Wizard configuration
####################

This configuration mode presents a wizard showing the configuration dialogs for
the selected nodes, one at a time. The nodes will be shown in dependency order
and the wizard makes sure that every preceding node is executed before each
selected node dialog.

Having the preceding nodes executed when configuring is useful when the content
of the dialogs depends on data, for example, the column names in the input
table.

.. figure:: screenshot_subflow_wizard_configuration.png
   :alt: Example subflow wizard configuration
   :align: center

   Subflow wizard configuration. This workflow can be found in `<sympathy install
   directory>/Sympathy/Doc/workflows/ADAF example with subflow.syx`.
   First check "Use wizard configuration" to configure in this way.


.. _`Linked Subflows`:

Linked Subflows
^^^^^^^^^^^^^^^

Ordinary subflows are integrated into your workflow, and are stored within the
same workflow file. If you have made a very useful subflow you may want to use
that in several different workflows or many times in the same workflow. You
could of course simply copy your subflow but maintaining it would become
cumbersome since any update that you wanted to do in the subflow will have to
be made manually in all copies of the subflow.

Instead you can create a linked subflow by right-clicking on the subflow and
selecting *Refactor->Save subflow as link*. This will prompt you to save the subflow to a
file and the containing workflow will now only store a link to the subflow.
This is indicated by a pair of links of a chain on the outside of the subflow.

If you edit a linked subflow and save the changes any workflow that you open
which contains a link to that subflow will also see those changes.

.. warning::
   Note that the contents of any linked subflows are only read when you open a
   workflow. Meaning that if you already have a workflow containing a link to
   the subflow open when you make a change in the subflow, that workflow might
   not see the change until you close and reopen the workflow.


Parameter overrides
###################

The default setting when configuring a linked subflow is to override the base
parameters with the new configuration. These overrides are stored in the
flow containing the subflow and thus do not affect the linked subflow file. This
can be very useful when you want to use a subflow many times but with slightly
different configurations. Each place where you use it will link to the same
workflow file, but will use different overrides.

Note that configuring a node which has override directly will also only change
the overrides. Similarly, when copying a node with overrides, the pasted node
will have the active override parameters as its only parameters.

You can remove the overrides for a specific node by deselecting it in the
subflow settings. If you have a specific use case where overriding parameters
is not what you need you can also disable it in the subflow settings.
Configuring the subflow will then change the nodes directly, and will thus
affect the linked-in workflow file.


.. _locked_subflows:

Locked Subflows
^^^^^^^^^^^^^^^

Locked subflows are executed in one process without generating intermediate
files for the purpose of faster execution. They are recognized by the *no sign*
icon (a circle with backslash inside) and also by the fact that there are no
numbers in the left corner showing the number of executed nodes inside divided
by total number of nodes. Inside normal subflows they count as a single node.

When executed from the outside, all of the nodes inside are
executed. Afterwards, any change of the configuration or content will cause the
state to reset back to *Armed*.  It can sometimes be useful to think of subflows
like normal nodes, but built from other nodes.  Like normal nodes, you mainly
use them from the outside. Editing the inside of a locked flow, in Sympathy,
would then correspond to editing the source code for a normal node. Locking
subflows can help speed up the execution by avoiding costly disk
operations. When editing the inside of a locked subflow it will behave like a
normal subflow.

The only node ports of locked subflows that are written to disk (and generate
intermediate files) are output ports from nodes connected to the top level *Flow
Output* ports of the locked flow. Advanced: if such a node has several outputs
of which only a few are connected to *Flow Output* ports it can, in some cases,
be useful to insert :ref:`org.sysess.sympathy.generic.propagatefirst` nodes to
avoid unnecessary disk operations.

Locking and unlocking of subflows is done in the context menu for subflows. It
is accessed by right-clicking and choosing *Advanced->Execution mode->Locked*. A
check mark in context menu item indicates that the subflow is currently locked.

.. figure:: screenshot_locked_normal_outside.png
   :alt: Outside comparison of locked and normal subflows.
   :align: center

   Shows a normal subflow above a locked subflow. Compare their different icons
   and observe that the number of executed nodes divided by total number of
   nodes is only shown for the normal subflow.

.. _`node_states_locked`:

Node states
###########

In addition to the most common states for nodes, see :ref:`node_states_base`,
nodes executed in locked subflows have a separate state to indicate that that
they are different from normally executed nodes and do not allow you to click on
their ports to inspect their output data.  The table below shows details for the
special state for nodes executed in locked mode.

+-------------------+--------------+------------+--------------------------------------------+
| State             | Color        | State icon | Explanation                                |
+===================+==============+============+============================================+
| `Done locked`     | Light purple | Check mark | Successfully executed without disk output. |
+-------------------+--------------+------------+--------------------------------------------+

.. figure:: screenshot_locked_inside_executed.png
   :alt: Inside view of a executed locked subflow.
   :align: center

   Shows the immediate inside of a locked subflow that has been executed from
   the outside.  The icon from the outside view appears as a light watermark in
   the background.  The input node (*Random Table*) is show as *Done locked* in
   light purple and the output node (*Select columns in Table*) is simply
   *Done*.

.. warning::
   Note that executing in locked mode can significantly increase
   memory use, since data on intermediate output ports that would otherwise have
   been written to disk is kept in memory.

.. _flows_in_library:

Subflows in the Node Library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Subflows can be used to build new nodes for third party libraries. This can be
accomplished by saving them with filenames matching flow_*.syx in a library
folder. The identifier field needs to be set on the top level flow (Right-click
-> Preferences: General section). Subflows used as nodes will be linked using the
identifier instead of the filename. To avoid clashes, use an identifier in the
following format: <library-identifier>.<flow-identifier>. This is the same
format that should be used for nodes.
