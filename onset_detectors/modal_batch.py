#!/usr/bin/env python
import sys
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import modal
import modal.onsetdetection as od
import modal.ui.plot as trplot

def computeOnsetsModal(f):
    file_name = f
    sampling_rate, audio = wavfile.read(file_name)
    audio = np.asarray(audio, dtype=np.double)
    audio /= np.max(audio)

    frame_size = 2048
    hop_size = 512

    #odf = modal.EnergyODF()
    #odf = modal.SpectralDifferenceODF()
    odf = modal.ComplexODF() #default examples


    #odf = modal.LinearPredictionODF()
    #odf = modal.LPEnergyODF()
    #odf = modal.LPSpectralDifferenceODF()
    #odf = modal.LPComplexODF()
    #odf = modal.LPEnergyODF()
    #odf = modal.LPSpectralDifferenceODF()
    #odf = modal.LPComplexODF()
    #odf = modal.PeakODF()
#    odf = modal.UnmatchedPeaksODF()
#    odf = modal.PeakAmpDifferenceODF()

    odf.set_hop_size(hop_size)
    odf.set_frame_size(frame_size)
    odf.set_sampling_rate(sampling_rate)
    odf_values = np.zeros(len(audio) / hop_size, dtype=np.double)
    odf.process(audio, odf_values)

    #There's only one peak picker
    onset_det = od.OnsetDetection()
    onset_det.peak_size = 3
    onsets = onset_det.find_onsets(odf_values) * odf.get_hop_size()

    return onsets

#Parse command line arguments
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

		#Call your processing function here
        onsets = computeOnsetsModal(f)

        print onsets
        onsetsSecs = onsets / 44100.0
        
        np.savetxt(outFile, onsetsSecs, fmt='%f')
        
if __name__ == '__main__':
    main()
