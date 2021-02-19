.. _vcfTabix:

vcfTabix example
----------------
You can read more about preparing the files necessary for a vcfTabix track
on `UCSC's bigInteract help page
<https://genome.ucsc.edu/goldenPath/help/vcf.html>`_. The following code
uses the example files provided by UCSC.

This code is automatically run and the built trackhub is uploaded to the
`trackhub-demo <https://github.com/daler/trackhub-demo>`_ repository. You can
view the live hub using `this link <http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=https://raw.githubusercontent.com/daler/trackhub-demo/master/example_vcfTabix_hub/vcfTabix.hub.txt&position=chr21:33034804-33037719>`_.

.. code-block:: python

    import trackhub

    hub, genome, genomes_file,trackdb = trackhub.default_hub(
        hub_name = 'vcfTabix',
        short_label = 'vcfTabix_example',
        long_label = 'vcfTabix_example',
        genome = 'hg19',
        defaultPos = 'chr21:33034804-33037719',
        email = 'eva.jason@nih.gov')

    track = trackhub.Track(
        tracktype = 'vcfTabix',
        name = 'vcfTabix',
        chromosomes = 'chr21',
        visibility = 'pack',
        bigDataUrl = 'http://genome.ucsc.edu/goldenPath/help/examples/vcfExample.vcf.gz')
    trackdb.add_tracks(track)

    trackhub.upload.upload_hub(hub = hub, host = 'localhost',remote_dir = 'example_hubs/example_vcfTabix_hub')
