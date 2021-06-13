import glob
import os
import os.path as op

import pytest

TEST_DIR = op.join(op.abspath(op.dirname(__file__)), 'testfiles')


@pytest.fixture
def chafiles():
    testfiles = glob.glob(f'{TEST_DIR}/*.cha')
    outfiles = [
        f'{fn}_out' + f'{ext}' for (fn, ext) in [
            op.splitext(p) for p in testfiles
        ]
    ]
    yield zip(testfiles, outfiles)
    for f in outfiles:
        if op.exists(f):
            os.remove(f)
