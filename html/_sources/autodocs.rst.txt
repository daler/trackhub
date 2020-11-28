.. _autodoc:

API documentation
=================

.. rubric:: Classes:

.. autosummary::
    :toctree: autodocs
    :template: auto_template

    trackhub.base.HubComponent
    trackhub.Hub
    trackhub.GenomesFile
    trackhub.Genome
    trackhub.TrackDb
    trackhub.BaseTrack
    trackhub.Track
    trackhub.CompositeTrack
    trackhub.ViewTrack
    trackhub.SuperTrack
    trackhub.AggregateTrack
    trackhub.SubGroupDefinition
    trackhub.params.Parameter

.. rubric:: Classes specific to assembly hubs:

.. autosummary::
    :toctree: autodocs
    :template: auto_template

    trackhub.GroupsFile
    trackhub.GroupDefinition
    trackhub.Assembly

.. rubric:: Functions

.. autosummary::
    :toctree: autodocs

    trackhub.upload.stage_hub
    trackhub.upload.upload_hub
    trackhub.helpers.dimensions_from_subgroups
    trackhub.helpers.filter_composite_from_subgroups
    trackhub.helpers.hex2rgb
    trackhub.helpers.sanitize
    trackhub.helpers.data_dir

