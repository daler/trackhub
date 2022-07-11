# To run a single test that matches a string, use:
#
#   pytest ad_hoc_test.py -k <string>

from trackhub.track import ViewTrack, CompositeTrack, ParameterError
import pytest

def test_view_params():
    # ViewTracks are required to have a tracktype kwarg, so this should raise
    # track.ParameterError
    with pytest.raises(ParameterError):
        v = ViewTrack(view='testing', name='testnameview')

def test_view_track_allows_bigwig_kwargs():
    v = ViewTrack(view='testnameview', name='testview', tracktype='bigWig', viewLimits='5:50')
    str(v)

def test_composite_track_allows_bigwig_kwargs():
    c = CompositeTrack(name='testnamecomp', tracktype='bigWig', viewLimits='5:50')
    str(c)

# Eva to test:
# Does the browser allow a composite track to have no tracktype set?
def test_composite_track_should_allow_no_track_type():
    c = CompositeTrack(name='testnamecomp')
    str(c)


def test_bw_kwargs_color():
    c = CompositeTrack(comp='test',name='testnamecomp',tracktype='bigWig',color='119,10,233')


def test_example_passing():
    assert 1 == 1

def test_view_without_composite():

