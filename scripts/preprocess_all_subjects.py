#!/usr/bin/env python3

import subprocess
import sys
import argparse
from util.io.iter_BIDSPaths import *

def main(subs, skips) -> None:
    BIDS_ROOT = '../data/bids'
    layout = BIDSLayout(BIDS_ROOT, derivatives = False)
    fpaths = layout.get(extension = 'eeg',
                        return_type = 'filename')

    for (fpath, sub, task, run) in iter_BIDSPaths(fpaths):
        # if subs were given but sub is not in subs, don't preprocess
        if bool(subs) and sub not in subs:
            continue
        # if sub in skips, don't preprocess
        if sub in skips:
            continue
        subprocess.check_call("sbatch ./preprocess.py %s %s %s" % (sub, task, run), shell=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run preprocess.py over given subjects')
    parser.add_argument('--subs', type = str, nargs = '*', help = 'subjects to preprocess (e.g. 3 14 8), provide no argument to run over all subjects', default = [])
    parser.add_argument('--skips', type = str, nargs = '*', help = 'subjects NOT to preprocess (e.g. 1 9)', default = [])
    args = parser.parse_args()
    subs = args.subs
    skips = args.skips
    print(f"subs: {subs}, skips : {skips}")
    if bool(subs) & bool(skips):
        raise ValueError('Cannot specify both subs and skips')
    main(subs, skips)
