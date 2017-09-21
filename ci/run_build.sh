#!/bin/bash

set -e

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


(
  cd $HERE


    python build_example.py

    # TODO: communicate between build_example and this script to configure
    # which directory to use.
    REMOTE_FN="example_hub"

    if [[ $TRAVIS == "true" ]]; then
        # Set up ssh key for push access on travis-ci.
        #
        # References:
        #  - https://docs.travis-ci.com/user/encrypting-files
        #  - https://gist.github.com/domenic/ec8b0fc8ab45f39403dd
        #
        ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
        ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
        ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
        ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
        ENCRYPTED_FILE=${HERE}/key.enc
        openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in .$ENCRYPTED_FILE -out key -d
        chmod 600 key
        eval `ssh-agent -s`
        ssh-add key
    fi


    SSH_REPO="git@github.com:daler/trackhub-demo.git"
    rm -rf trackhub-demo
    git clone $SSH_REPO

    # We want the trackhub-demo repo's branch to match the current branch of
    # trackhub, so grab the current trackhub branch now before we move to
    # trackhub-demo.
    BRANCH=$(git rev-parse --abbrev-ref HEAD)

    (
        set -x
        cd trackhub-demo

        git checkout -B $BRANCH
        cp -r $REMOTE_FN trackhub-demo

        if git diff --quiet; then
            echo "No changes to push"
        else
            git add -f .
            git commit -m "update hub"
            git push origin $BRANCH
        fi
        set +x
    )

    if [[ ! -e hubCheck ]]; then
        curl -O http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/hubCheck
        chmod +x hubCheck
    fi
    echo "Checking hub..."
    set -x; ./hubCheck https://raw.githubusercontent.com/daler/trackhub-demo/${TRACKHUB_BRANCH}/my_example_hub.txt; set +x
)
