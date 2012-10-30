import os
import subprocess
import pybedtools
from trackhub import helpers

data_dir = helpers.data_dir()

chromsizes = pybedtools.genome_registry.dm3.euchromatic
g = pybedtools.chromsizes_to_file(chromsizes)

# Make some randomized bigBed files
for i in range(3):
    x = pybedtools.BedTool(
        "chr2L 0 10000000", from_string=True)\
        .window_maker(w=1000 * (i + 1))\
        .shuffle(g=g, seed=i)\
        .sort()

    out = os.path.join(data_dir, 'random-dm3-%s.bigBed' % i)

    cmds = [
        'bedToBigBed',
        x.fn,
        g,
        out]
    p = subprocess.Popen(cmds)
    p.communicate()


# make some sine waves for bigWigs
import numpy as np
def sine(factor):

    for chrom, size in chromsizes.items():
        _, size = size
        x = np.arange(0, size, 10000)
        y = np.sin(x / factor / np.pi) + np.random.random(len(x)) / 3
        for xi, yi in zip(x, y):
            yield pybedtools.create_interval_from_list(map(str, [
                chrom, xi, xi + 1000, yi]))

for f in [1000., 10000.]:
    x = pybedtools.BedTool(sine(f)).saveas(os.path.join(data_dir, 'sine-dm3-%d.bedgraph' % f))
    out = x.fn + '.bw'

    cmds = [
        'bedGraphToBigWig',
        x.fn,
        g,
        out]
    p = subprocess.Popen(cmds)
    p.communicate()
    os.unlink(x.fn)

