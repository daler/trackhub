import os
import subprocess
import pybedtools
import numpy as np
from trackhub import helpers

np.random.seed(0)

data_dir = helpers.data_dir()

with open('chromsizes', 'w') as fout:
    fout.write('chr1\t10000\n')

# First, make some example BED files to convert to bigBed


for i, x in enumerate([
    pybedtools.BedTool(
        """
        chr1 10 50
        chr1 100 125
        chr1 300 400
        """, from_string=True),
    pybedtools.BedTool(
        """
        chr1 500 600
        """, from_string=True),
    pybedtools.BedTool(
        """
        chr1 20 60
        chr1 40 100
        chr1 80 90
        chr1 250 300
        """, from_string=True)
]):
    out = os.path.join(data_dir, 'random-hg38-%s.bigBed' % i)
    cmds = [
        'bedToBigBed',
        x.fn,
        'chromsizes',
        out]
    subprocess.check_call(cmds)

# make some sine waves for bigWigs



def sine(resolution=10, power=2):
    resolution = 10
    x = np.arange(0, 10000, resolution)
    y = np.sin(x / resolution ** power) + np.random.random(x.shape[0])
    for xi, yi in zip(x, y):
        yield pybedtools.create_interval_from_list([
            'chr1',
            str(xi),
            str(xi + resolution),
            '{0:.3f}'.format(yi)
        ])


for i, x in enumerate([
    sine(resolution=10, power=2.0),
    sine(resolution=10, power=2.5),
    sine(resolution=10, power=3.0),
]):
    x = pybedtools.BedTool(x).saveas(os.path.join(data_dir, 'sine-hg38-%d.bedgraph' % i))
    out = x.fn + '.bw'
    cmds = [
        'bedGraphToBigWig',
        x.fn,
        'chromsizes',
        out]
    subprocess.check_call(cmds)
    os.unlink(x.fn)

os.unlink('chromsizes')
