#!/bin/bash

set -eou pipefail

set -x
# References:
#  - https://docs.travis-ci.com/user/encrypting-files
#  - https://gist.github.com/domenic/ec8b0fc8ab45f39403dd

# ----------------------------------------------------------------------------
#
# Repository-specific configuration
#
# ----------------------------------------------------------------------------

# Note that the keypair needs to be specific to repo, so if ORIGIN changes, the
# keypair (docs/key.enc, and the corresponding public key in the setting of the
# repo) need to be updated.
BRANCH="gh-pages"
ORIGIN="trackhub"
GITHUB_USERNAME="daler"

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# DOCSOURCE is directory containing the Makefile, relative to the directory
# containing this bash script.
DOCSOURCE=${HERE}/../doc

# DOCHTML is where sphinx is configured to save the output HTML
DOCHTML=${HERE}/../doc/build/html

# tmpdir to which built docs will be copied
STAGING=/tmp/${GITHUB_USERNAME}-docs

ENCRYPTED_FILE=${HERE}/docs-key.enc

# Build docs only if travis-ci is testing this branch:
BUILD_DOCS_FROM_BRANCH="master"

# ----------------------------------------------------------------------------
#
# END repository-specific configuration. The code below is generic; to use for
# another repo, edit the above settings.
#
# ----------------------------------------------------------------------------
set +u
if [[ $TRAVIS != "true" ]]; then
    echo "Not running on travis; exiting cleanly"
    exit 0
fi
set -u

# Decrypt and ssh-add key.
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL_DOCS}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL_DOCS}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in $ENCRYPTED_FILE -out key -d
chmod 600 key
eval `ssh-agent -s`
ssh-add key

# clone the branch to tmpdir, clean out contents
rm -rf $STAGING
mkdir -p $STAGING
SSH_REPO="git@github.com:${GITHUB_USERNAME}/${ORIGIN}.git"
SHA=$(git rev-parse --verify HEAD)
git clone $SSH_REPO $STAGING
cd $STAGING
git checkout $BRANCH || git checkout --orphan $BRANCH
rm -r *

# build docs and copy over to tmpdir
cd ${DOCSOURCE}
make clean html 2>&1 | grep -v "WARNING: nonlocal image URL found:"
cp -r ${DOCHTML}/* $STAGING

# commit and push
cd $STAGING
touch .nojekyll
git add .nojekyll

# committing with no changes results in exit 1, so check for that case first.
if git diff --quiet; then
    echo "No changes to push -- exiting cleanly"
    exit 0
fi

if [[ $TRAVIS_BRANCH != $BUILD_DOCS_FROM_BRANCH ]]; then
    echo "Not pushing docs because not on branch '$BUILD_DOCS_FROM_BRANCH'"
    exit 0
fi

if [[ $TRAVIS_PULL_REQUEST != "false" ]]; then
    echo "This is a pull request, so not pushing docs"
    exit 0
fi

if [[ $TRAVIS_REPO_SLUG != "daler/trackhub" ]]; then
    echo "On a fork of the main trackhub repo, so not pushing docs"
    exit 0
fi


# Add, commit, and push
echo ".*" >> .gitignore
git config user.name "Travis CI"
git config user.email "${GITHUB_USERNAME}@users.noreply.github.com"
git add -A .
git commit --all -m "Updated docs to commit ${SHA}."
echo "Pushing to $SSH_REPO:$BRANCH"
git push $SSH_REPO $BRANCH &> /dev/null
