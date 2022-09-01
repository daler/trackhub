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

To create a template, run:

``python trackhub_from_excel.py --template``

Optionally, you can provide a name for your Excel file:

``python trackhub_from_excel.py --template RNAseq_experiment.xlsx``

2. Fill out the Excel workbook
------------------------------

Using the template just created, fill out the sheets with the data you'd like
to visualize.

hub and genome sheets
~~~~~~~~~~~~~~~~~~~~~

**hub** – This sheet is necessary for all track hubs. It
defines the hub name and labels and genome.

**genome** – This sheet is only necessary when using a genome assembly. It
points the 2bit file and gives the genome a name and labels.

Container track sheets
~~~~~~~~~~~~~~~~~~~~~~

Container tracks must be configured in their own sheet.

Use these sheet names when using the corresponding container track:

- aggregate_config
- view_config
- super_config
- composite_config

Each type of container track must be on its own sheet. The sheet label
“view_config” can have several view tracks defined but there can be no other
types of container tracks defined on that sheet. This applies to all container
track types. All other sheets can have any name (they should not contain the
word “config”). These sheets are used for the actual data tracks. 

Special fields for container track configuration:

Aggregate – An aggregate track can be placed in a super track. In this case,
include the name of the super track in the “super” column.

View – This track must be placed inside of a composite track. Include the name
of the composite track in the column labeled “composite”.

Composite – A composite track can be placed in a super track. In this case,
include the name of the super track in the column labeled “super”.

Super tracks are within the track hub and therefore do not need special fields.

Subgroups
~~~~~~~~~

To add a subgroup to a track, make a column with the prefix “subgroup\_”. The value after the underscore will become the name of the subgroup. Fill in the group that data file fits into. 

For example, to make subgroups based on genotype, you might label the column “subgroup_genotype” and fill in the rows with “WT” or “MT”. You can make several subgroups.

Tracks
~~~~~~

Each row defines a track and must have the “name”, “tracktype”, and “source” or “bigDataUrl” fields. Use “source” when the file is on disk and use “bigDataUrl” when the file is publicly hosted. The user can define more fields according to the specific track type.

Different track types can be listed on the same sheet. Tracks in different containers can be listed on the same sheet and tracks in the same containers can be listed on different sheets.

Leave the cell in the Excel sheet blank to omit that track field for that track. The program will remove this field for the track.

To use container tracks, be sure to define the container and use the “container” and “container_type” fields for the track. 

For example, to place a track in a view track you need first add a row for the view in the view_config. In another sheet, fill out a row for the track including the “container_type” and “container” fields. For column labeled “container_type” fill in “view” and for the column labeled “container” fill in the same name that is in the view_config sheet.

3. Run the script
-----------------

This will default to naming the track hub directory as “staging”

``python trackhub_from_excel.py --excel_file experiment.xlsx``

You can run it with the ``--staging`` flag to specify the name

``python trackhub_from_excel.py --excel_file experiment.xlsx --staging experiment``
