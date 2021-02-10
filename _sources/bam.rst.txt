.. _bam_example:

bam example
-----------
You can read more about preparing the files necessary for a bam track
on `UCSC's bam help page
<https://genome.ucsc.edu/goldenPath/help/bam.html>`_. The following code uses the example files provided by UCSC.


This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgHubConnect?hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgHub_do_firstDb=1&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_assembly_hub/assembly_hub.hub.txt&position=chr14%3A95060967%2D95501030>`_.

.. code-block:: python

     import trackhub
     hub, genomes_file, genome, trackdb = trackhub.default_hub(
          hub_name="bam",
          short_label="bam",
          long_label="bam",
          genome="hg18",
          defaultPos = "chr21:33038946-33039092",
          email="eva.jason@nih.gov")

     track = trackhub.Track(
          tracktype='bam',
          name="bam",
          description="bam ex. 1: 1000 genomes read alignments (individual na12878)",
          pairEndsByName=".",
          pairSearchRange='10000',
          chromosomes='chr21',
          maxWindowToDraw='200000',
          visibility='pack',
          bigDataUrl='http://genome.ucsc.edu/goldenPath/help/examples/bamExample.bam')
     trackdb.add_tracks(track)
     trackhub.upload.upload_hub(hub=hub, host="localhost", remote_dir="example_hubs/example_bam_hub")
