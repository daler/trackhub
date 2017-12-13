import os
import hashlib
from trackhub import helpers

def test_example_data_md5s():
    data_dir = helpers.data_dir()

    data = [i.strip().split() for i in '''
    ba2fd8b22bcad65bb6583da937ff5222  newOrg1.2bit
    35fa6ac3453e2bbd503c40a1d15afc65  random-hg38-0.bigBed
    3c94c294f8376f625f3701dee7641997  random-hg38-1.bigBed
    3bed0726e452d677f33979b2ed1c65d6  random-hg38-2.bigBed
    ca19fa98f532c883117e6c79ca77741f  random-no1-0.bigBed
    b909ad9c25de1e51db649b177edeb90f  random-no1-1.bigBed
    1066162e223e7b5a14b05f1d119332b1  random-no1-2.bigBed
    3735b696b3a416a59f8755eaf5664e5a  sine-hg38-0.bedgraph.bw
    73ad8ba3590d0895810d069599b0e443  sine-hg38-1.bedgraph.bw
    85478d1ecc5906405ccb43d1ca426d29  sine-hg38-2.bedgraph.bw
    55ac2603c31b232dacfdaba07d8a25eb  sine-no1-1000.bedgraph.bw
    b8c983862c58fee6afa99382634ab2d8  sine-no1-100.bedgraph.bw
    '''.splitlines(False) if len(i.strip()) > 0]

    success = True
    for md5, fn in data:
        fn = os.path.join(data_dir, fn)
        obs = hashlib.md5(open(fn, 'rb').read()).hexdigest()
        success = success and (obs == md5)
        print(obs, md5, fn)
    assert success
