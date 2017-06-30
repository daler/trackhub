from trackhub import *
from trackhub.track import *
import os
import inspect

def test_parentonoff():

    hub, genomes_file, genome, trackdb = default_hub( 
        hub_name = "TestHub", 
        short_label="TestHub", 
        long_label="TestHub", 
        email="karen.kapur@novartis.com", 
        genome="hg19"
    ) 
    ## Write files locally; need to be placed in accessible location
    hub.local_fn="hub.txt"
    genomes_file.local_fn="genomes.txt"

    testcomposite = CompositeTrack( 
        name="testcomposite",
        short_label="testlabelshort", 
        long_label="testlabellong", 
        tracktype="bigWig", 
        visibility="full"
    )

    viewtrack = ViewTrack(
        name = "testviewtrack", 
        view = "view1", 
        tracktype = "bigWig", 
        visibility = "full"
    )

    trackoff = Track(
        name = "E003DNase", 
        url= "http://egg2.wustl.edu/roadmap/data/byFileType/signal/consolidated/macs2signal/pval/E003-DNase.pval.signal.bigwig",
        tracktype="bigWig",
        short_label="E003DNase",
        long_label = "E003DNase",
        visibility = "full",
        parentonoff = "off"
        )
    trackon = Track(
        name = "E004DNase", 
        url= "http://egg2.wustl.edu/roadmap/data/byFileType/signal/consolidated/macs2signal/pval/E004-DNase.pval.signal.bigwig",
        tracktype="bigWig",
        short_label="E004DNase",
        long_label = "E004DNase",
        visibility = "full",
        parentonoff = "on"
        )
    trackdefault = Track(
        name = "E005DNase", 
        url= "http://egg2.wustl.edu/roadmap/data/byFileType/signal/consolidated/macs2signal/pval/E005-DNase.pval.signal.bigwig",
        tracktype="bigWig",
        short_label="E005DNase",
        long_label = "E005DNase",
        visibility = "full"
        )


    viewtrack.add_tracks( trackoff )  
    viewtrack.add_tracks( trackon )  
    viewtrack.add_tracks( trackdefault )  
        
    
    testcomposite.add_view( viewtrack )
    trackdb.add_tracks( testcomposite )

    results = hub.render()

    assert( open( 'trackhub/test/test_parentonoff/hg19/trackDb.txt').read() == open('trackhub/test/test_parentonoff/expected/hg19/trackDb.txt').read() )

