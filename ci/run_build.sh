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


# Keys are the directory in the trackhub-demo repo that you'd like to store
# them in. Values are the path to the hub.txt. The dirname of the hub.txt will
# be copied into the trackhub-demo repo.
declare -A hubs
hubs["example_hub"]="example_hub/myhub.hub.txt"
hubs["example_assembly_hub"]="example_assembly_hub/assembly_hub.hub.txt"
hubs["example_grouping_hub"]="example_grouping_hub/grouping.hub.txt"
hubs["example_htmldoc_hub"]="example_htmldoc_hub/htmldoc.hub.txt"
hubs["example_barchart_hub"]="example_barchart_hub/barchart_hub.hub.txt"
hubs["quickstart"]="../doc/quickstart-staging/quickstart.hub.txt"


# We want the trackhub-demo repo's branch to match the current branch of
# trackhub, so grab the current trackhub branch now before we move to
# trackhub-demo repo
BRANCH=$(git rev-parse --abbrev-ref HEAD)

(

  # Clean existing hubs first
  cd $HERE

  for hub in "${!hubs[@]}"; do
      rm -rf $hub
  done

  # Rebuild examples.
  #
  # The README is plain vanilla ReST, so we can't use .. testcode:: directives
  # in it, and therefore must parse manually. The quickstart example is
  # doctested, so that gets run by the make doctest...
  (cd $HERE/../doc && make doctest)

  # ...but the others in the `hubs` array get built using `build_example.py`.
  python build_example.py

  # Clone the trackhub-demo repo and move those just-built hubs over.
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

  set +e
  set -x

  ALL_OK=0
  for hub in "${!hubs[@]}"; do
      pth=$(basename ${hubs[$hub]})

      # hubCheck exits 1 even with just warnings.
      ./hubCheck https://raw.githubusercontent.com/daler/trackhub-demo/${BRANCH}/$hub/$pth > /tmp/$hub.log
      cat /tmp/$hub.log

      if grep -Ev "warning|Found" /tmp/$hub.log; then
        ALL_OK=1
        echo $hub >> /tmp/problems
        cat /tmp/$hub.log >> /tmp/problems
      fi

  done

  if [[ $ALL_OK == 1 ]]; then
      cat /tmp/problems
      exit 1
  fi

  for hub in "${!hubs[@]}"; do
      pth=$(dirname ${hubs[$hub]})
      rm -r $pth
  done

  # clean up
  rm -rf $HERE/trackhub-demo

)
