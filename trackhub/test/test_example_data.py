import os
import hashlib
from trackhub import helpers

def test_example_data_md5s():
    data_dir = helpers.data_dir()

    data = [i.strip().split() for i in '''
    ba2fd8b22bcad65bb6583da937ff5222 newOrg1.2bit
    eef35bd42b79885b168e9613f2e20e27 random-dm3-0.bigBed
    10d37b0c1bf784ff2106b9c3dd802e3a random-dm3-1.bigBed
    f298dbe95d865f8a0c618c87b1027def random-dm3-2.bigBed
    ca19fa98f532c883117e6c79ca77741f random-no1-0.bigBed
    b909ad9c25de1e51db649b177edeb90f random-no1-1.bigBed
    1066162e223e7b5a14b05f1d119332b1 random-no1-2.bigBed
    94cb83c18f73b713878c6ef28c19087d sine-dm3-10000.bedgraph.bw
    968df78a8a18c6e7d5b061e92fde8d83 sine-dm3-1000.bedgraph.bw
    55ac2603c31b232dacfdaba07d8a25eb sine-no1-1000.bedgraph.bw
    b8c983862c58fee6afa99382634ab2d8 sine-no1-100.bedgraph.bw
    '''.splitlines(False) if len(i.strip()) > 0]

    success = True
    for md5, fn in data:
        fn = os.path.join(data_dir, fn)
        obs = hashlib.md5(open(fn, 'rb').read()).hexdigest()
        success = success and (obs == md5)
        print(obs, md5, fn)
    assert success
