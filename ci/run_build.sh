#!/bin/bash
set -e

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

BRANCH="master"
ORIGIN="master"
GITHUB_USERNAME="dalerr"
ENCRYPTED_FILE=${HERE}/key.enc

(
  cd $HERE

    if [[ ! -e hubCheck ]]; then
        wget -O- http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/hubCheck > hubCheck
        chmod +x hubCheck
    fi

    python build_example.py

    REMOTE_FN="example_hub"

    if [[ $TRAVIS == "true" ]]; then
        # Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
        ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
        ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
        ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
        ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
        openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in .$ENCRYPTED_FILE -out key -d
        chmod 600 key
        eval `ssh-agent -s`
        ssh-add key
    fi
    # Now that we're all set up, we can push.
    SSH_REPO="git@github.com:daler/trackhub-demo.git"
    rm -rf trackhub-demo
    git clone $SSH_REPO

    TRACKHUB_BRANCH=$(git rev-parse --abbrev-ref HEAD)

    (
        set -x
        cd trackhub-demo
        git fetch
        git checkout -B $TRACKHUB_BRANCH
        git pull origin $TRACKHUB_BRANCH

        cp -r $REMOTE_FN trackhub-demo

        if git diff --quiet; then
            echo "No changes to push"
        else
            git add -f .
            git commit -m "update hub"

            git push origin $TRACKHUB_BRANCH
        fi
        set +x
    )

    echo "Checking hub..."
    set -x; ./hubCheck https://raw.githubusercontent.com/daler/trackhub-demo/${TRACKHUB_BRANCH}/my_example_hub.txt; set +x
)
