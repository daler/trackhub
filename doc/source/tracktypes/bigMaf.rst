.. _bigMaf:

bigMaf example
--------------
You can read more about preparing the files necessary for a bigGenePred track
on `UCSC's bigMaf help page
<https://genome.ucsc.edu/goldenPath/help/bigMaf.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgHubConnect?hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgHub_do_firstDb=1&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigMaf_hub/bigMaf_hub.hub.txt&position=chr14%3A95060967%2D95501030>`_.

.. code-block:: python

     import trackhub

     hub, genome, genomes_file,trackdb = trackhub.default_hub(
          hub_name='bigMaf',
          short_label='bigMaf',
          long_label='bigMaf',
          genome='hg38',
          email='eva.jason@nih.gov')

     track = trackhub.Track(
          name = 'bigMaf',
          frames= 'http://genome.ucsc.edu/goldenPath/help/examples/bigMafFrames.bb',
          bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigMaf.bb',
          tracktype='bigMaf')
     trackdb.add_tracks(track)
     
     trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_bigMaf_hub')
