#!/usr/bin/env python

import sys
import argparse
import subprocess as sp
from pathlib import Path

# Figure out what branch we're on
p = sp.run('git branch | grep "*"', shell=True, stdout=sp.PIPE, universal_newlines=True)
detected_branch = p.stdout.lstrip("*").strip()

# Find the abs path of the TSV to use
tsv = (Path(__file__).parent / "example_hubs.tsv").absolute()

ap = argparse.ArgumentParser()
ap.add_argument(
    "--branch",
    default=detected_branch,
    help="Branch to check on trackhub-demo repo. Defaults to current branch in this (trackhub) repo, which is '%(default)s'",
)
ap.add_argument(
    "--tsv",
    default=tsv,
    help="TSV from which to pull example hubs, default is %(default)s",
)
args = ap.parse_args()

# Download hubCheck if needed and make executable
hubcheck = Path("hubCheck")
if not Path(hubcheck).exists():
    sp.run(
        ["curl", "-O", "http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/hubCheck"]
    )
    hubcheck.chmod(0o700)

for line in open(args.tsv):
    line = line.strip()
    if line.startswith('#') or not line:
        continue

    # Dest in trackhub demo is the second column of TSV, without the initial directory
    dest = line.split("\t")[1]
    dest = Path(dest)
    dest = Path(*dest.parts[1:])

    URL = f"https://raw.githubusercontent.com/daler/trackhub-demo/{args.branch}/{dest}"
    print("checking", URL, "...")
    res = sp.run(
        ["./hubCheck", URL], stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True
    )

    # hubCheck has exit code 1 even if there are only warnings. So we look for
    # those and handle them appropriately.
    error = False
    warnings = False
    if res.returncode:
        for line in res.stdout.splitlines():
            if not (line.startswith("Found") or line.startswith("warning:")):
                error = True
            else:
                warnings = True

    if warnings:
        print("Warnings found, but considering this OK:")
        print(res.stdout)

    if error:
        print(f"Error in hub {URL}:")
        print(res.stdout)

        # Exit immediately
        sys.exit(1)
