from __future__ import absolute_import, print_function

import tempfile
import os
from fabric.api import local, settings, run, abort, cd, env, hide, puts
from fabric.contrib.console import confirm
from fabric.colors import green, yellow
from . import track


def upload_file(host, user, local_fn, remote_fn, port=22,
                rsync_options='-azvrL --progress', run_local=False,
                symlink=False, symlink_dir='staging'):
    results = []
    puts('\n\n' + green(local_fn) + ' -> ' +  yellow(remote_fn))
    if symlink:
        symlink_dest = os.path.join(symlink_dir, remote_fn)
        os.system('mkdir -p %s' % (os.path.dirname(symlink_dest)))
        remote_dir = os.path.dirname(remote_fn)
        os.system('ln -sf %s %s' % (os.path.abspath(local_fn), symlink_dest))
        local_fn = symlink_dest

    if run_local:
        if not os.path.exists(os.path.dirname(remote_fn)):
            remote_dir = os.path.dirname(remote_fn)
            if remote_dir:
                results.append(local('mkdir -p %s' % remote_dir))

        results.append(local('rsync %(rsync_options)s %(local_fn)s %(remote_fn)s' % locals()))
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


def upload_hub(host, user, hub, port=22, rsync_options='-azvrL --progress',
               run_local=False, symlink=False, symlink_dir='staging'):
    kwargs = dict(host=host, user=user, port=port, rsync_options=rsync_options,
                  run_local=run_local, symlink=symlink, symlink_dir=symlink_dir)
    print(kwargs)
    results = []

    # First the hub file:
    results.extend(
        upload_file(
            local_fn=hub.local_fn,
            remote_fn=hub.remote_fn,
            **kwargs)
    )

    # Then the genomes file:
    print(hub.genomes_file.local_fn)
    results.extend(
        upload_file(
            local_fn=hub.genomes_file.local_fn,
            remote_fn=hub.genomes_file.remote_fn,
            **kwargs)
    )

    # Then any associated trackDb:
    for g in hub.genomes_file.genomes:
        results.extend(
            upload_file(
                local_fn=g.trackdb.local_fn,
                remote_fn=g.trackdb.remote_fn,
                **kwargs
            )
        )

        # and assemblies
        if hasattr(g, "local_fn"):
            results.extend(
                upload_file(
                    local_fn=g.local_fn,
                    remote_fn=g.remote_fn,
                    **kwargs
                )
            )

        if getattr(g, "groups", None) != None:
            results.extend(
                upload_file(
                    local_fn=g.groups.local_fn,
                    remote_fn=g.groups.remote_fn,
                    **kwargs
                )
            )

        if hasattr(g, '_html') and g._html:
            results.extend(
                upload_file(
                    local_fn=g._html.local_fn,
                    remote_fn=g._html.remote_fn,
                    **kwargs)
            )

    # and finally any HTML files:
    for t, level in hub.leaves(track.CompositeTrack, intermediate=True):
        print(repr(t))
        if t._html:
            results.extend(
                upload_file(
                    local_fn=t._html.local_fn,
                    remote_fn=t._html.remote_fn,
                    **kwargs)
            )
    return results


def upload_track(host, user, track, port=22, rsync_options='-azvrL --progress',
                 run_local=False):
    kwargs = dict(host=host, user=user, local_fn=track.local_fn,
                  remote_fn=track.remote_fn, rsync_options=rsync_options,
                  run_local=run_local)
    results = upload_file(**kwargs)
    if track.tracktype == 'bam':
        kwargs['local_fn'] += '.bai'
        kwargs['remote_fn'] += '.bai'
        results.extend(upload_file(**kwargs))

    if track.tracktype == 'vcfTabix':
        kwargs['local_fn'] += '.tbi'
        kwargs['remote_fn'] += '.tbi'
        results.extend(upload_file(**kwargs))
    return results
