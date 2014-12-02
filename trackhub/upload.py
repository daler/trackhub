import tempfile
import os
from fabric.api import local, settings, run, abort, cd, env, hide, put
from fabric.contrib.console import confirm
import track
import boto
from boto.s3.key import Key


def upload_s3(local_fn, remote_fn, **kwargs):
    s3 = boto.connect_s3()
    bucket = s3.get_bucket("sauron-yeo")
    k = Key(bucket)
    k.key = remote_fn
    k.set_contents_from_filename(local_fn)
    k.make_public()
    return ["done"]


def upload_file(host, user, local_fn, remote_fn, port=22,
                rsync_options='-azvr --progress', run_local=False):
    results = []
    if run_local:
        if not os.path.exists(os.path.dirname(remote_fn)):
            results.append(local('mkdir -p %s' % os.path.dirname(remote_fn)))

        results.append(local('rsync -avr --progress %(local_fn)s %(remote_fn)s' % locals()))
        return results
    env.host_string = host
    env.user = user
    env.port = port

    remote_dir = os.path.dirname(remote_fn)

    with settings(warn_only=True):
        result = run('ls %s' % remote_dir)

    if result.failed:
        run('mkdir -p %s' % remote_dir)

    rsync_template = \
        'rsync %(rsync_options)s %(local_fn)s %(user)s@%(host)s:%(remote_fn)s'
    with settings(warn_only=True):
        results.append(local(rsync_template % locals()))
    return results


def upload_hub(host, user, hub, port=22, rsync_options='-azvr --progress',
               run_local=False, run_s3=False):
    kwargs = dict(host=host, user=user, port=port, rsync_options=rsync_options,
                  run_local=run_local)
    print kwargs
    results = []
    if run_s3:
        cur_upload_file = upload_s3
    else:
        cur_upload_file = upload_file
    # First the hub file:
    results.extend(
        cur_upload_file(
            local_fn=hub.local_fn,
            remote_fn=hub.remote_fn,
            **kwargs)
    )

    # Then the genomes file:
    print hub.genomes_file.local_fn
    results.extend(
        cur_upload_file(
            local_fn=hub.genomes_file.local_fn,
            remote_fn=hub.genomes_file.remote_fn,
            **kwargs)
    )

    # then the trackDB file:
    for g in hub.genomes_file.genomes:
        results.extend(
            cur_upload_file(
                local_fn=g.trackdb.local_fn,
                remote_fn=g.trackdb.remote_fn,
                **kwargs
            )
        )
    # and finally any HTML files:
    for t, level in hub.leaves(track.CompositeTrack, intermediate=True):
        print repr(t)
        if t._html:
            results.extend(
                cur_upload_file(
                    local_fn=t._html.local_fn,
                    remote_fn=t._html.remote_fn,
                    **kwargs)
            )
    return results


def upload_track(host, user, track, port=22, rsync_options='-azvr --progress',
                 run_local=False, run_s3=False):

    if run_s3:
        cur_upload_file = upload_s3
    else:
        cur_upload_file = upload_file
    kwargs = dict(host=host, user=user, local_fn=track.local_fn,
                  remote_fn=track.remote_fn, rsync_options=rsync_options,
                  run_local=run_local)
    results = cur_upload_file(**kwargs)
    if track.tracktype == 'bam':
        kwargs['local_fn'] += '.bai'
        kwargs['remote_fn'] += '.bai'
        results.extend(upload_file(**kwargs))

    return results
