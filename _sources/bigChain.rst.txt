.. _bigChain:

bigChain example
----------------
You can read more about preparing the files necessary for a bigChain track
on `UCSC's bigBarChart help page
<https://genome.ucsc.edu/goldenPath/help/barChain.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgHubConnect?hgHub_do_redirect=on&hgHubConnect.remakeTrackHub=on&hgHub_do_firstDb=1&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigChain_hub/bigChain_hub.hub.txt&position=chr14%3A95060967%2D95501030>`_.

.. code-block:: python

     import trackhub

     hub, genomes_file, genome, trackdb = trackhub.default_hub(
          hub_name='bigChain',
          short_label='bigChain',
          long_label='bigChain',
          genome='hg38',
          defaultPos = 'chr22:1-150754',
          email='eva.jason@nih.gov')

     track = trackhub.Track(
          name = 'bigChain',
          bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigChain.bb',
          shortLabel = 'bigChain',
          longLabel ='bigChain Example Hub',
          tracktype = 'bigChain',
          visibility = 'pack')
     trackdb.add_tracks(track)
     
     trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_bigChain_hub')
