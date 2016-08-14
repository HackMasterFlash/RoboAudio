#!/usr/bin/env python
"""
RoboAudio.py -- Start of my tool suite to convert mp3 audio to binary data that I can then analyze to try to generate
music with similar characteristics. I'm going to start small.

Usage:
    $ ./RoboAudio.py

    Script will prompt for input mp3 file.
"""
import string
import sys
import Tkinter
#from tkFileDialog import askopenfile
from tkFileDialog import askopenfilename
from scipy.io import wavfile
import pydub
import numpy as np
import scipy.signal as signal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def dumpWAV( name ):
    sound = pydub.AudioSegment.from_mp3(name)
    name1 = str.split(name, '.')
    name2 = string.join(name1[: len(name1) - 1]) + ".wav"
    sound.export(name2, format="wav")
    print("Wrote %s" % name2)
    return name2

def ReadWavToData(wavName):
    [rate, data] = wavfile.read(wavName)
    rightChannel = []
    leftChannel = []

    print("Loading data into numpy arrays")
    print("Data size = %i" % len(data))
    i = 0
    for element in data:
        rightChannel.append(element[0])
        leftChannel.append(element[1])
        i = i + 1
        if i % 1000000 == 0:
            print("Percent Read %0.1f" % (100.0*(i/float(len(data)))) )
    return [rate, np.array(leftChannel), np.array(rightChannel)]

def ProcessData( rate, Left, Right):
    """Calculate & display frequency content of song"""
    f, Pwelch_spec = signal.welch(Left[100000:165536], rate, scaling='spectrum')
    print("Size f = %i" % len(f))
    print("len Left = %i" % len(Pwelch_spec))
    plt.plot(f, Pwelch_spec )
    plt.xlabel('frequency [Hz]')
    plt.ylabel('PSD')

    f, Pper_spec = signal.periodogram(Left[100000:165536], rate, 'blackman', scaling='spectrum')
    plt.plot(f, Pper_spec)
    plt.grid()
    plt.show()

def main(filename):
    """The main function in this script/class"""
    print("Reading file %s" % filename)
    wavName = dumpWAV(filename)
    [ rate, Left, Right] = ReadWavToData(wavName)
    ProcessData( rate, Left, Right)

if __name__ == '__main__':
    print('Python %s on %s' % (sys.version, sys.platform))
    filename = "test.mp3"
    if len(sys.argv) == 1:
        print("Select an mp3 file")
        root = Tkinter.Tk()
        root.withdraw()
        filename = askopenfilename(parent=root, filetypes=[("Mp3 files", "*.mp3")])
        #inputFile = askopenfile() #filetypes=[("text files", "*.TXT")]
        #filename = inputFile.name
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print( __doc__)
        sys.exit()
    main(filename)