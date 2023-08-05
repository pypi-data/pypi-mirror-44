.. _editor-beakdowns:

===================
 Editor Breakdowns
===================

There is an editor for every BEAT object:

* Databases
* Libraries
* Dataformats
* Algorithms
* Toolchains
* Experiments
* Plotters
* Plotterparameters

Some of these editors are more complex than others - if you can't figure something out, look here!

.. note:: If the images are too small, right-click on the image in your browser and click `View Image` to see the image in another tab at full resolution!

.. _generic-editor-features:

Generic Editor Features
=======================

.. image:: ./img/editor_generic_breakdown.png

1. `Object Name`: The name of the object being edited.
2. `Validity Flag`: Whether the object as it is in your prefix has JSON metadata that is considered valid by the BEAT system.
3. `Path to object in filesystem`: The absolute path on your filesystem to the object's files.
4. `Editor tab`: The tab that displays the user-friendly editor for the specific object.
5. `JSON tab`: The tab that displays the object's raw JSON metadata (this is the metadata edited in the Editor tab).
6. `Save Changes button`: Saves all the changes you've made to the object to your prefix. Also has a small Validity flag indicating whether or not your unsaved changes are valid.
7. `Python file generation button`: Generates a Python file based off a template for the object's type. This button is only available when editing objects of types that have Python files associated with them.
8. `Description field`: A short description of the object.

.. _database-editor:

Database Editor
===============

.. image:: ./img/editor_database_breakdown.png

1. `Root Folder field`: The absolute path to the root folder for the data files for this database. This folder is used inside the BEAT system to provide the data files to the database Python code when indexing/executing the database views.
2. `Active Protocol`: Databases can have multiple protocols, but you only edit one at a time. The active protocol is shown, while the others are hidden. The active protocol in this image is "Main".
3. `Protocol Switcher`: A dropdown which lets you switch to other protocols.
4. `Protocol Delete, Clone, and Create buttons`: Buttons to delete, clone, and create protocols. _Delete_ and _Clone_ operate on the active protocol. _Clone_ and _Create_ automatically switch the active protocol to the new protocol.
5. `Protocol Template Insert field`: Search and insert a protocol based on the protocol template name from any database in your prefix.
6. `Protocol Name field`: Change the protocol's name.
7. `Protocol Template field`: Change the protocol's template name.
8. `Protocol Template Warning`: If the active protocol has a template name which is shared by at least one other protocol in any database with different contents, this warning pane will show the protocol names & associated databases. This warning shows because every protocol with the same template name should have the exact same sets/outputs/inputs/parameters.
9. `New Set button`: Add a new set to the protocol.
10. `Protocol Set`: A protocol has sets, each of which are shown in succession. The first set in this image is "training", the second is "testing".
11. `Set Delete & Clone buttons`: Buttons to delete or clone the set.
12. `Set Name field`: Field to change the set's name.
13. `Set Template field`: Field for changing the set's template name.
14. `Set View Name field`: Field for entering the name of the Python View class to use for this set.
15. `New Set Parameter button`: Creates a new parameter for the set, each of which having a name and a string value.
16. `New Set Output button`: Creates a new output for the set.
17. `Output Name field`: Field for changing the output's name.
18. `Output dataformat field`: Field for selecting the output's dataformat.
19. `Quick Jump menu`: An overview of the protocols and sets in your database. Clicking on a protocol name will switch you to that protocol, and clicking on a set will jump you to that set. You can also create protocols & sets using the corresponding buttons.

.. _dataformat-editor:

Dataformat Editor
=================

.. image:: ./img/editor_dataformat_breakdown.png

1. `Fields`: Dataformats have fields, each with at least a name and a type (which could be any other dataformat, a dictionary, array, string, or number types).
2. `Field Name`: Change the field's (or subfield's) name.
3. `Field dataformat`: Select the field's type.
4. `Array dimensions`: Array-type (sub)fields have configurable dimensions, allowing for matrices and such.
5. `Array dimension restrictions`: You can restrict the lengths of a specific dimension. A value of "0" implies no restriction.
6. `Array field subtype`: Array fields have a subtype, which can be any valid type/dataformat.
7. `Dict field subfields`: Fields/subfields/array subtypes that are "dict" have subfields, allowing for arbitrarily complex dataformats.
8. `New Subfield button`: Each dict field can have any amount of subfields added to it.
9. `New Field button`: Dataformats can have any arbitrary amount of top-level fields.

.. _algorithm-editor:

Algorithm Editor
================

.. image:: ./img/editor_algorithm_breakdown.png

1. `Analyzer Flag`: Whether or not the algorithm is for analyzer blocks. If this flag is checked, a new algorithm tab, `Results`, will be available for adding & editing the result fields. These result fields are very similar to output fields in normal algorithm groups, but with restricted types. The algorithm shown in the image does not have this field checked, and so is not an analyzer algorithm.
2. `Splittable Flag`: Whether or not the algorithm is splittable (parallelizeable). Only available on non-analyzer algorithms.
3. `Endpoints tab`: The algorithm tab where the algorithm's groups & inputs & outputs are defined & edited.
4. `Parameters tab`: The algorithm tab where the algorithm's parameters are defined & edited.
5. `Libraries tab`: The algorithm tab where the algorithm's used BEAT libraries and their aliases are defined and edited.
6. `First Group`: All algorithms need at least one group, and the first group is the only group that can have outputs.
7. `Second Group`: All groups after the second group can only have inputs.
8. `Input Name field`: Field changing the group's input's name.
9. `Input Dataformat field`: Field changing the group's input's dataformat.
10. `Output Name field`: Field changing the group's output's name.
11. `Output Dataformat field`: Field changing the group's output's dataformat.
12. `New Input button`: Adds a new input to the group.
13. `New Output button`: Adds a new output to the group.
14. `Delete Group button`: Deletes the group. The first group cannot be deleted, because all algorithms require at least one group.

.. _toolchain-editor:

Toolchain Editor
================

.. image:: ./img/editor_toolchain_breakdown.png

1. `Toolchain Graphical Editor`: Below the "Description" field in the Toolchain Editor in a window showing a custom editor made to graphically edit toolchains. This is a scrollable window, with blocks laid on the lined background.
2. `Menu Bar`: This is the menu bar for the graphical editor, with several buttons to help use this tool:

   - Undo & Redo: Move backwards & forwards in editing history.
   - Layout: Uses graphviz's dot layout algorithm to calculate a cleaner and more pleasing toolchain layout given the blocks and connection info.
   - Zoom Out/In: Zooms out and in.
   - Fit: Fits the toolchain to the Graphical Editor window.
   - Pop Out/In: Expands the editor to almost fill your browser's tab, and shrinks it back down.
   - See Help: Pops open a help modal that shows you how to do things in the Graphical Editor.

3. `Dataset blocks`: Dataset blocks only have outputs, and are typically on the lefthand side of the toolchain. Each dataset provides its own synchronization channel, which is a different random color. Each block with the same color as a dataset block is synchronized to that dataset block.
4. `Normal Blocks`: Normal blocks have inputs and outputs and are typically in the middle of the toolchain.
5. `Input Connectors`: These black rectangles are where connections are attached to.
6. `Output Connectors`: These block rectangles are where connections are started from - click and drag on the rectangle to start a connection from that output.
7. `Analyzer Blocks`: Analyzer blocks only have inputs and typically are at the right end of the toolchain. Only 1 Analyzer should be in a toolchain.
8. `Connections`: Connections go from a block's output to another block's input. Connections are colored according to the synchronization channel of the block it starts from.
9. `Background Canvas`: The background canvas, where blocks can be moved or created.

How to use the Graphical Editor:

* Everything in the editor can be right-clicked to open a contextual menu about it.
* Left-click blocks to open the Block Editor modal where you change the block's names, inputs, outputs, and synchronization channel. Left-clicking and dragging moves blocks.
* Right-click on the background canvas to create blocks, insert them from existing toolchains, or insert them based off of an algorithm or database protocol.
* Select and operate on multiple blocks by shift-clicking blocks or by click-dragging an area select box. When any blocks are selected, all connections will be hidden except for those connected to/from the selected blocks. Click anywhere on the background canvas to dismiss the selection.

.. _experiment-editor:

Experiment Editor
=================

.. image:: ./img/editor_experiment_breakdown.png

1. `Toolchain Viewer`: This is a stripped-down, read-only version of the the graphical toolchain editor. It lets you see the toolchain for the experiment. Clicking on the background canvas will jump you to the Global Settings section.
2. `Dataset Blocks`: Clicking a dataset block will jump you to that dataset block's settings for this experiment.
3. `Normal & Analyzer Blocks`: Clicking a normal or analyzer block will pop up the block's settings and jump you to those settings.
4. `Type Inference Toggle button`: When selecting an algorithm or dataset for a block, the experiment editor will filter results to be compatible with adjacent blocks' algorithms or datasets, if they have chosen any. If Type Inference is toggled off, the editor won't filter options based on types.
5. `Current Block`: The settings for the last clicked block are shown here. The name of the block is given, as well as the synchronized channel.
6. `Execution Defaults Toggle`: By default, all blocks are executed in the Global Environment. If you need to override the block's environment, first toggle this.
7. `Environment Name Selector`: If the "Execution Defaults Toggle" is using the global defaults, this is disabled. If not, it lets you choose a docker environment available on your system to execute the block in.
8. `Block Algorithm Selector`: This lets you select an algorithm for the block. Only algorithms with the same number of inputs and outputs as the block will be allowed. If Type Inference is enabled and adjacent blocks have algorithms/datasets selected, the options will be further filtered.
9. `Copy Block button`: Will copy the block's settings to blocks that are similar (same except for the block name) and that have not already have had an algorithm chosen for it. Only available for normal blocks.
10. `Algorithm input/output name & type`: When you select an algorithm for a block, the Inputs & Outputs of the algorithm are shown (both the name and dataformat).
11. `Block input/output selector`: You must assign each input & output of the block to the correct input/output of the algorithm. The editor tries to assign them appropriately, but it's best to double-check.
12. `Protocol Selector`: As a shortcut for assigning datasets for your experiment, you may assign an entire protocol to all the dataset blocks at once, if any are available.
13. `Toolchain dataset info`: Each dataset block in the toolchain is listed here, giving its name and provided synchronization channel.
14. `Dataset Selector`: You need to assign a compatible set from a protocol from a database to each dataset block. The name format is "<Protocol>/<set> (<database>)".
15. `Global Environment Selector`: If you are using the docker executor, you may selector a docker environment to execute the experiment's blocks in.


.. automodule:: beat.editor
