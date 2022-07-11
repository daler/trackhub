import trackhub

trackhub.settings.VALIDATE = False
hub, genome, genomes_file,trackdb = trackhub.default_hub(
     hub_name='bigLolly',
     short_label='bigLolly',
     long_label='bigLolly',
     genome='hg38',
     defaultPos = 'chr21:25891755-25891870',
     email='eva.jason@nih.gov')

add_kwargs = {'yAxisLabel.1': '0 on 30,30,190 0',
              'yAxisLabel.1' : '5 on 30,30,190 5'}

track = trackhub.Track(
     tracktype = 'bigLolly',
     bigDataUrl= 'http://genome.ucsc.edu/goldenPath/help/examples/bigLollyExample3.bb',
     name = 'bigLolly',
     lollySizeField='lollySize',
     visibility='full',
     noStems='on',
     lollyMaxSize=10,
     **add_kwargs)
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost', remote_dir='example_hubs/example_bigLolly_hub')