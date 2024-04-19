.. currentmodule:: trackhub

.. _excelinstructions:

Track hub from Excel
====================

If you are an avid user of the UCSC Genome Browser and the *trackhub* package,
you might find it tedious to write a script for every single hub you create.
The command-line tool uses this package to further automate the trak hub making
process. Additionally, if you are not familiar with Python, this tool makes it
even easier to make track hubs. Follow this guide for how to use the package
and how to fill out an Excel workbook to make any simple or complex
visualization on the UCSC Genome Browser. 

1. Create a template
--------------------

The Excel file must have a specific format to be parsed correctly. 

To create a template, run::

    trackhub_from_excel --template

This will create a file ``template.xlsx`` in the current directory, with the
correct sheets that you can fill out with the instructions below.

Alternatively, you can get a working example to study and test::

    trackhub_from_excel --create-example my_example.xlsx

2. Fill out the Excel workbook
------------------------------

Using the template just created, fill out the sheets with the data you'd like
to visualize.

hub and genome sheets
~~~~~~~~~~~~~~~~~~~~~

The following special sheet names are used for configuring the hub and the
genome (for assembly tracks):

``hub`` – This sheet is necessary for all track hubs. It
defines the hub name and labels and genome.

``genome`` – This sheet is only necessary when using a genome assembly. It
points to the 2bit file and gives the genome a name and label.

Example ``hub`` sheet
`````````````````````

.. list-table::

    * - hub
      - examplehub
    * - short_label
      - Example hub
    * - long_label
      - Example track hub from Excel
    * - email
      - user@example.com
    * - genome
      - hg38


Container track sheets
~~~~~~~~~~~~~~~~~~~~~~

Container tracks must be configured in their own sheet.

The following special sheet names are required when using the corresponding
container track. These sheets are created in the template:
``aggregate_config``, ``view_config``, ``super_config``, and
``composite_config``.

Each type of container track must be on its own sheet. For example the sheet
``view_config`` can have several view tracks defined but there can be no other
types of container tracks defined on that sheet. This applies to all container
track types.

Columns in these sheets correspond to valid track parameters for the respective
track type. There are also some special fields for container track configuration:

Extra ``aggregate_config`` field: An aggregate track can be placed in a super
track. In this case, include add a super track in ``super_config``, and in
``aggregate_config`` add a ``super`` column and add the name of the super
track.

Extra ``view_config`` field: Views must be placed inside of a composite track. Configure
this by adding the name of the composite track in the column labeled
``composite``.

Extra ``composite_config`` field: A composite track can be placed in a super
track. In this case, include the name of the super track in the column labeled
``super`` similar to as described above for ``view_config``.

Super tracks are within the track hub and therefore do not need special fields.

.. note::

    Subgroups are not specified in the composite config. Rather, they are
    automatically inferred and created based on the subgroups assigned to
    individual tracks (and which composites those tracks are assigned to). This
    makes it much more convenient to organize your tracks. See the tracks
    section below for details.


Example ``view_config`` sheet
`````````````````````````````

.. list-table::
    :header-rows: 1

    * - name
      - view
      - short_label
      - long_label
      - visibility
      - tracktype
      - composite
    * - signal
      - signalview
      - Genomic signal
      - Genomic signal (CPM)
      - full
      - bigWig
      - experiment1
    * - peaks
      - peaksview
      - Peaks
      - Called peaks (macs2)
      - dense
      - bigBed
      - experiment1

Example ``composite_config`` sheet
``````````````````````````````````

.. list-table:: 
    :header-rows: 1

    * - name
      - short_label
      - long_label
      - tracktype
      - super
    * - experiment1
      - experiment 1
      - Experiment 1
      - bigWig
      - supertrack1
    * - experiment2
      - experiment 2
      - Experiment 2
      - bigWig
      - 

Example ``super_config`` sheet
``````````````````````````````

.. list-table::
    :header-rows: 1

    * - name
      - short_label
      - long_label
    * - supertrack1
      - Super track
      - Super track

Tracks
~~~~~~

All other sheets that do not have the special names indicated above are assumed
to configure tracks.

Each row defines a track and must have values in the ``name``, ``tracktype``,
and ``source`` (or ``bigDataUrl``) columns. Use ``source`` when the file is on
disk and use ``bigDataUrl`` when the file is publicly hosted. The user can
define more fields according to the specific track type.

Different track types can be listed on the same sheet. Tracks in different
containers can be listed on the same sheet and tracks in the same containers
can be listed on different sheets.

Leave the cell in the Excel sheet blank to omit that track field for that
track. The program will remove this field for the track.

To use container tracks, be sure to define the container and use the
``container`` and ``container_type`` fields for the track. 

For example, to place a track in a view track you need first add a row for the
view in the ``view_config`` sheet that includes a ``name`` field. In another
sheet (containing tracks, so you can name it whatever you want), fill out a row
for the track including the ``container_type`` and ``container`` fields in
addition to the required fields described above. For the ``container_type``
column, fill in "view" and for the ``container`` column fill in the same name
that is in the ``view_config`` sheet.

To add a subgroup to a track, make a column with the prefix ``subgroup_``. The
value after the underscore will become the name of the subgroup. Fill in the
group that data file fits into. 

For example, to make subgroups based on genotype, you might label the column
``subgroup_genotype`` and fill in the rows with "WT" or "KO". You can make
as many subgroups as you need.

Example ``tracks`` sheet
````````````````````````

.. list-table::
    :header-rows: 1

    * - name
      - short_label
      - long_label
      - tracktype
      - source
      - visibility
      - color
      - container
      - container_type
      - dimensions
      - subgroup_celltype
      - subgroup_genotype
    * - k562_wt
      - K562 WT signal
      - K562 cells, WT signal
      - bigWig
      - data/kwt.bigwig
      - full
      - 120,51,154
      - signalview
      - view
      - dimX=genotype dimY=celltype
      - k562
      - wt
    * - k562_wt_pk
      - K562 WT peaks
      - K562 cells, WT peaks
      - bigBed
      - data/kwt.bigbed
      - dense
      - 120,51,154
      - peakview
      - view
      - dimX=genotype dimY=celltype
      - k562
      - wt



3. Run the script
-----------------

This will default to naming the track hub directory as “staging”

``python trackhub_from_excel.py --excel_file experiment.xlsx``

You can run it with the ``--staging`` flag to specify the name

``python trackhub_from_excel.py --excel_file experiment.xlsx --staging experiment``

The output directory will then be ready for uploading to a host.
