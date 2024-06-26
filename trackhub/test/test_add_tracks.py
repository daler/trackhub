import trackhub


def test_composite_args():
    """Tests to see if different types can be handled by 'add_tracks' in the class CompositeTrack"""

    c1 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    t1 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    t2 = trackhub.track.Track(name="testtrack2", tracktype="bigWig")
    v1 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")

    d = {"track1": t1, "track2": t2}

    c1 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    c1.add_tracks(v1, [t1, t2])
    res1 = str(c1)

    c2 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    c2.add_tracks(v1, t1, t2)
    res2 = str(c2)

    c3 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    c3.add_tracks(v1, d.values())
    res3 = str(c3)

    c4 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    c4.add_tracks(t1, [v1, t2])
    res4 = str(c4)

    assert res1 == res2 == res3 == res4


def test_agg_args():
    """Tests for backward compatibility. Compares the output of the
    old method 'add_subtracks' with the new one 'add_tracks' in the class AggregateTrack."""

    a1 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    t1 = trackhub.track.Track(name="test", tracktype="bigWig")
    a1.add_tracks(t1)
    agg1 = str(a1)

    a2 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    t2 = trackhub.track.Track(name="test", tracktype="bigWig")
    a2.add_subtrack(t2)
    agg2 = str(a2)

    assert agg1 == agg2


def test_add_multiple_agg_args():
    """Tests to see if different object types can be handled by 'add_tracks' in the class AggregateTrack."""

    t1 = trackhub.track.Track(name="test", tracktype="bigWig")
    t2 = trackhub.track.Track(name="test", tracktype="bigWig")
    t3 = trackhub.track.Track(name="test", tracktype="bigWig")

    a1 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    a1.add_tracks(t1, t2, t3)
    agg1 = str(a1)

    a2 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    a2.add_tracks([t1, t2, t3])
    agg2 = str(a2)

    a3 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    a3.add_tracks(t1, [t2, t3])
    agg3 = str(a3)

    a4 = trackhub.track.AggregateTrack(
        name="testagg", tracktype="bigWig", aggregate="transparentOverlay"
    )
    dagg = {"t1": t1, "t2": t2, "t3": t3}
    a4.add_tracks(dagg.values())
    agg4 = str(a4)

    assert agg1 == agg2 == agg3 == agg4


def test_composite_tracks():
    """Tests for backwards compatibility. Compares the old methods 'add_view' and 'add_subtrack'
    with the new one 'add_tracks' in the class CompositeTrack."""

    c1 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    t1 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    v1 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")
    c1.add_tracks(t1)
    c1.add_tracks(v1)

    assert isinstance(v1, trackhub.track.ViewTrack)
    assert c1.views == [v1]

    c2 = trackhub.track.CompositeTrack(name="testcomposite", tracktype="bigWig")
    t2 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    v2 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")
    c2.add_subtrack(t2)
    c2.add_view(v2)

    results1 = str(c1)
    results2 = str(c2)

    assert (
        results1
        == results2
        == """track testcomposite
shortLabel testcomposite
longLabel testcomposite
type bigWig
subGroup1 view Views v=v
compositeTrack on

    track a
    shortLabel a
    longLabel a
    type bigWig
    parent testcomposite
    view v

    track testtrack
    shortLabel testtrack
    longLabel testtrack
    type bigWig
    parent testcomposite"""
    )


def test_super_track():
    """Tests to see if different object types can be handled by 'add_tracks' in the class SuperTrack
    and that it produces the same result as before it was updated"""

    t1 = trackhub.track.Track(name="test1", tracktype="bigWig")
    t2 = trackhub.track.Track(name="test2", tracktype="bigWig")
    t3 = trackhub.track.Track(name="test3", tracktype="bigWig")

    s1 = trackhub.track.SuperTrack(name="super")
    s1.add_tracks(t1, t2, [t3])
    sup1 = str(s1)

    s2 = trackhub.track.SuperTrack(name="super")
    s2.add_tracks([t1, t2, t3])
    sup2 = str(s2)

    s3 = trackhub.track.SuperTrack(name="super")
    s3.add_tracks(t1, t2, t3)
    sup3 = str(s3)

    s4 = trackhub.track.SuperTrack(name="super")
    dsup = {"t1": t1, "t2": t2, "t3": t3}
    s4.add_tracks(dsup.values())
    sup4 = str(s4)

    assert (
        sup1
        == sup2
        == sup3
        == sup4
        == """track super
shortLabel super
longLabel super
type superTrack
superTrack on

    track test1
    shortLabel test1
    longLabel test1
    type bigWig
    parent super

    track test2
    shortLabel test2
    longLabel test2
    type bigWig
    parent super

    track test3
    shortLabel test3
    longLabel test3
    type bigWig
    parent super"""
    )


def test_add_tracks_view():
    """Tests to see if different object types can be handled by 'add_tracks' in the class ViewTrack
    and that it produces the same result as before it was updated"""

    t1 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    t2 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    t3 = trackhub.track.Track(name="testtrack", tracktype="bigWig")
    v1 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")
    v2 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")
    v3 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")
    v4 = trackhub.track.ViewTrack(name="a", view="v", tracktype="bigWig")

    v1.add_tracks([t1, t2, t3])
    view1 = str(v1)

    v2.add_tracks(t1, [t2, t3])
    view2 = str(v2)

    v3.add_tracks(t1, t2, t3)
    view3 = str(v3)

    dview = {"t1": t1, "t2": t2, "t3": t3}
    v4.add_tracks(dview.values())
    view4 = str(v4)

    assert (
        view1
        == view2
        == view3
        == view4
        == """track a
shortLabel a
longLabel a
type bigWig
view v

    track testtrack
    shortLabel testtrack
    longLabel testtrack
    type bigWig
    parent a
    subGroups view=v

    track testtrack
    shortLabel testtrack
    longLabel testtrack
    type bigWig
    parent a
    subGroups view=v

    track testtrack
    shortLabel testtrack
    longLabel testtrack
    type bigWig
    parent a
    subGroups view=v"""
    )
