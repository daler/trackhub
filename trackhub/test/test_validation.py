import trackhub
import pytest

def test_issue_20():
    t = trackhub.Track(name='a', tracktype='bigBed', priority=1)
    with pytest.raises(trackhub.validate.ValidationError):
        print(t)
    t = trackhub.Track(name='a', tracktype='bigBed', priority=1.0)
    print(t)
