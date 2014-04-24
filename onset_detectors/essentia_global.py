#!/usr/bin/env python

# Copyright (C) 2006-2013  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/
import sys
import numpy as np

from essentia import Pool, array
from essentia.standard import *


# In this example we are going to look at how to perform some onset detection
# and mark them on the audio using the AudioOnsetsMarker algorithm.
#
# Onset detection consists of two main phases:
#  1- we need to compute an onset detection function, which is a function
#     describing the evolution of some parameters, which might be representative
#     of whether we might find an onset or not
#  2- performing the actual onset detection, that is given a number of these
#     detection functions, decide where in the sound there actually are onsets


def computeOnsets(inFile, outFile):

    # don't forget, we can actually instantiate and call an algorithm on the same line!
    print 'Loading audio file...'
    audio = MonoLoader(filename = inFile)()

    pool = Pool()

    onsetDetectionGlobal = OnsetDetectionGlobal()
    onsetDetections = onsetDetectionGlobal(audio)

    pool.add('features.onsetDetections', onsetDetections)

    onsets = Onsets()
    onsetTimes = onsets(array([onsetDetections]), [1] )

    pool.add('features.onsets', onsetTimes)
    np.savetxt(outFile, pool['features.onsets'][0], fmt='%f')

def parser():
    import argparse

    p = argparse.ArgumentParser()

    p.add_argument('files', metavar='files', nargs='+',
                   help='files to be processed')

    p.add_argument('-v', dest='verbose', action='store_true',
                   help='be verbose')

        # parse arguments
    args = p.parse_args()
    # print arguments
    if args.verbose:
        print args
    # return args
    return args

def main():
    import os.path
    import glob
    import fnmatch
    # parse arguments
    args = parser()
    # determine the files to process
    files = []
    for f in args.files:
        # check what we have (file/path)
        if os.path.isdir(f):
            # use all files in the given path
            files = glob.glob(f + '/*.wav')
        else:
            # file was given, append to list
            files.append(f)
    # only process .wav files
    files = fnmatch.filter(files, '*.wav')
    files.sort()

    for f in files:
        if args.verbose:
            print f
        # use the name of the file without the extension
        filename = os.path.splitext(f)[0]

        outFile = "%s.onsets.txt" % (filename)

        computeOnsets(f, outFile)
        

if __name__ == '__main__':
    main()
