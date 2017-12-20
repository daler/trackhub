#!/bin/bash

# This driver script runs a full end-to-end test, including uploading to the
# trackhub-demo branch and running hubCheck on it.
#
#  - calls build_example.py, which:
#      - extracts the example out of the README
#      - runs it and generates a new trackhub in `example_hub` directory
#
#  - checks out a matching branch of the trackhub-demo repo
#  - copies over `example_hub` to trackhub-demo, then adds, commits, and pushes it
#  - downloads a copy of hubCheck if needed
#  - runs hubCheck on the newly pushed hub on trackhub-demo

set -e

HERE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

declare -A hubs

# Keys are the directory in the trackhub-demo repo that you'd like to store
# them in. Values are the path to the hub.txt. The dirname of the hub.txt will
# be copied into the trackhub-demo repo.
hubs["example_hub"]="example_hub/myhub.hub.txt"
hubs["example_assembly_hub"]="example_assembly_hub/assembly_hub.hub.txt"
hubs["example_grouping_hub"]="example_grouping_hub/grouping.hub.txt"
hubs["example_htmldoc_hub"]="example_htmldoc_hub/htmldoc.hub.txt"
hubs["quickstart"]="../doc/quickstart-staging/quickstart.hub.txt"

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
    openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in $ENCRYPTED_FILE -out key -d
    chmod 600 key
    eval `ssh-agent -s`
    ssh-add key
fi

# We want the trackhub-demo repo's branch to match the current branch of
# trackhub, so grab the current trackhub branch now before we move to
# trackhub-demo repo
if [[ ! -z $TRAVIS_BRANCH ]]; then
  BRANCH=$TRAVIS_BRANCH
else
  BRANCH=$(git rev-parse --abbrev-ref HEAD)
fi

(
  cd $HERE

  for hub in "${!hubs[@]}"; do
      rm -rf $hub
  done

  # Rebuild examples.
  #
  # The README is plain vanilla ReST, so we can't use .. testcode:: directives
  # in it, and therefore must parse manually. The quickstart example is
  # doctested, so that gets run by the make doctest.
  (cd $HERE/../doc && make doctest)
  python build_example.py

  SSH_REPO="git@github.com:daler/trackhub-demo.git"
  rm -rf trackhub-demo
  git clone $SSH_REPO

  (
      set -x
      cd trackhub-demo
      git checkout -B $BRANCH
      git rm -rf ./*

      # Make sure to use -L to follow symlinks
      for hub in "${!hubs[@]}"; do
          pth=${hubs[$hub]}
          hubdir=$(dirname $pth)
          cp -L -r ../$hubdir $hub
      done

      git add -f .
      if git diff origin/$BRANCH --quiet; then
          echo "no changes to push"
      else
          git commit -m "update hub"
          git push origin $BRANCH --force
      fi
      set +x
  )

  # Download hubCheck if we need it
  if [[ ! -e hubCheck ]]; then
      curl -O http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/hubCheck
      chmod +x hubCheck
  fi

  echo "Checking hubs..."

  for hub in "${!hubs[@]}"; do
      pth=$(basename ${hubs[$hub]})
      set -x; ./hubCheck https://raw.githubusercontent.com/daler/trackhub-demo/${BRANCH}/$hub/$pth; set +x
  done

  for hub in "${!hubs[@]}"; do
      pth=$(dirname ${hubs[$hub]})
      rm -r $pth
  done

  #rm -rf $HERE/trackhub-demo

)
