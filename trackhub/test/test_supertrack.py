"""
There can be multiple nested levels of tracks under super tracks. Here, we make
them all and test that the output is as expected.
"""


import trackhub

def test_supertrack():
    hub, genomes_file, genome, trackdb = trackhub.default_hub(
        hub_name="supertrack",
        short_label='example supertrack hub',
        long_label='example supertrack hub',
        genome="hg38",
        email="dalerr@nih.gov")

    trackdb.add_tracks(
        trackhub.Track(
            url='https://google.com',
            tracktype='bigWig',
            name='top_level_track')
    )

    supertrack = trackhub.SuperTrack(
        name='super',
        short_label='Super track'
    )
    trackdb.add_tracks(supertrack)

    supertrack.add_tracks(
        trackhub.Track(
            url='https://google.com',
            tracktype='bigWig',
            name='under_supertrack')
    )

    overlay = trackhub.AggregateTrack(
        aggregate='transparentOverlay',
        visibility='full',
        tracktype='bigWig',
        viewLimits='-2:2',
        maxHeightPixels='8:80:128',
        showSubtrackColorOnUi='on',
        name='agg_under_supertrack')
    supertrack.add_tracks(overlay)

    overlay.add_subtrack(
        trackhub.Track(
            url='https://google.com',
            tracktype='bigWig',
            name='track_under_agg_under_supertrack')
    )

    composite = trackhub.CompositeTrack(name='composite_under_supertrack', tracktype='bigWig')
    view = trackhub.ViewTrack(name='view', view='viewtrack', tracktype='bigWig')

    view.add_tracks(
        trackhub.Track(
            url='https://google.com',
            tracktype='bigWig',
            name='track_under_view')
    )
    composite.add_view(view)


    composite.add_subtrack(
        trackhub.Track(
            url='https://google.com',
            tracktype='bigWig',
            name='track_under_composite')
    )
    supertrack.add_tracks(composite)


    orig_indent = trackhub.constants.INDENT
    trackhub.constants.INDENT = '  '
    results = str(trackdb)
    trackhub.constants.INDENT = orig_indent

    expected = \
"""track top_level_track
bigDataUrl https://google.com
shortLabel top_level_track
longLabel top_level_track
type bigWig

track super
shortLabel Super track
longLabel Super track
type superTrack
superTrack on

  track under_supertrack
  bigDataUrl https://google.com
  shortLabel under_supertrack
  longLabel under_supertrack
  type bigWig
  parent super

  track agg_under_supertrack
  shortLabel agg_under_supertrack
  longLabel agg_under_supertrack
  type bigWig
  aggregate transparentOverlay
  maxHeightPixels 8:80:128
  parent super
  showSubtrackColorOnUi on
  viewLimits -2:2
  visibility full
  container multiWig

    track track_under_agg_under_supertrack
    bigDataUrl https://google.com
    shortLabel track_under_agg_under_supertrack
    longLabel track_under_agg_under_supertrack
    type bigWig
    parent agg_under_supertrack

  track composite_under_supertrack
  shortLabel composite_under_supertrack
  longLabel composite_under_supertrack
  type bigWig
  parent super
  subGroup1 view Views viewtrack=viewtrack
  compositeTrack on

    track view
    shortLabel view
    longLabel view
    type bigWig
    parent composite_under_supertrack
    view viewtrack

      track track_under_view
      bigDataUrl https://google.com
      shortLabel track_under_view
      longLabel track_under_view
      type bigWig
      parent view
      subGroups view=viewtrack

    track track_under_composite
    bigDataUrl https://google.com
    shortLabel track_under_composite
    longLabel track_under_composite
    type bigWig
    parent composite_under_supertrack
"""
    with open('super.test.observed', 'w') as fout:
        fout.write(results)

    with open('super.test.expected', 'w') as fout:
        fout.write(expected)

    assert results == expected

