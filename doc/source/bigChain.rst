.. _bigChain:

bigChain example
----------------
You can read more about preparing the files necessary for a bigChain track
on `UCSC's bigChain help page
<https://genome.ucsc.edu/goldenPath/help/bigChain.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg38&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_bigChain_hub/bigChain.hub.txt&position=chr22_KI270731v1_random>`_.

.. code-block:: python

     import trackhub

     hub, genomes_file, genome, trackdb = trackhub.default_hub(
          hub_name='bigChain',
          short_label='bigChain',
          long_label='bigChain',
          genome='hg38',
          email='eva.jason@nih.gov')

     track = trackhub.Track(
          name = 'bigChain',
          bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/bigChain.bb',
          linkDataUrl='http://genome.ucsc.edu/goldenPath/help/examples/bigChain.link.bb',
          shortLabel = 'bigChain',
          longLabel ='bigChain Example Hub',
          tracktype = 'bigChain',
          visibility = 'pack')
     trackdb.add_tracks(track)
     
     trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_bigChain_hub')
