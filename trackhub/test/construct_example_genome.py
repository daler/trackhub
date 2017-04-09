import os
import random
import subprocess
from collections import OrderedDict
import pybedtools
import numpy as np
from trackhub import helpers

random.seed(0)
np.random.seed(0)

data_dir = helpers.data_dir()

chromsizes = OrderedDict([
    ("chr1", (0, 100000)),
    ("chr2", (0, 75000)),
    ("chr3", (0, 50000))
])


def random_dna(length, chars="ATGC"):
    return ''.join(random.choice(chars) for _ in range(length)) + "\n"

fasta = open(os.path.join(data_dir, "newOrg1.fa"), "w")

for chrom, size in chromsizes.items():
    fasta.write(">" + chrom + "\n")
    n, r = divmod(size[1], 80)
    for _ in range(n):
        fasta.write(random_dna(80))
    fasta.write(random_dna(r))

cmds = [
    "faToTwoBit",
    fasta.name,
    fasta.name[0:-2] + "2bit"
]

p = subprocess.check_call(cmds)

fasta.close()
os.unlink(fasta.name)

g = pybedtools.chromsizes_to_file(chromsizes)

# Make some randomized bigBed files
for i in range(3):
    x = pybedtools.BedTool(
        "chr1 0 100000", from_string=True)\
        .window_maker(g=g, w=100 * (i + 1))\
        .shuffle(g=g, seed=i)\
        .sort()

    out = os.path.join(data_dir, 'random-no1-%s.bigBed' % i)

    cmds = [
        'bedToBigBed',
        x.fn,
        g,
        out]
    p = subprocess.check_call(cmds)


# make some sine waves for bigWigs
def sine(factor):

    for chrom, size in chromsizes.items():
        _, size = size
        x = np.arange(0, size, 10000)
        y = np.sin(x / factor / np.pi) + np.random.random(len(x)) / 3
        for xi, yi in zip(x, y):
            yield pybedtools.create_interval_from_list(list(map(str, [
                chrom, xi, xi + 1000, yi])))

for f in [100., 1000.]:
    x = pybedtools.BedTool(sine(f)).saveas(os.path.join(data_dir, 'sine-no1-%d.bedgraph' % f))
    out = x.fn + '.bw'

    cmds = [
        'bedGraphToBigWig',
        x.fn,
        g,
        out]
    p = subprocess.check_call(cmds)
    os.unlink(x.fn)
