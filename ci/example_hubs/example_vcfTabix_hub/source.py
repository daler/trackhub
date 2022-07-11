import trackhub

hub, genome, genomes_file,trackdb = trackhub.default_hub(
    hub_name = 'vcfTabix',
    short_label = 'vcfTabix_example',
    long_label='vcfTabix_example',
    genome='hg19',
    defaultPos = 'chr21:33034804-33037719',
    email='eva.jason@nih.gov')

track = trackhub.Track(
    tracktype = 'vcfTabix',
    name="VCF_Example_One",
    chromosomes='chr21',
    visibility='pack',
    url='http://genome.ucsc.edu/goldenPath/help/examples/vcfExample.vcf.gz')
trackdb.add_tracks(track)

trackhub.upload.upload_hub(hub=hub, host='localhost',remote_dir='example_hubs/example_vcfTabix_hub')