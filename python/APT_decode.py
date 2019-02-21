#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code for APT decode for NOAA satelites

Translated from matlab code by Guilherme Theis

@author: Guillame Ferré
@license: MIT
"""

import numpy as np # for numerical and mathematics
from matplotlib import pyplot as plt # for plotting
from scipy import signal # for DSP
from scipy.io import wavfile # for wav files reading
import argparse

 #-------------- Argparse for bash inputs --------------#
parser = argparse.ArgumentParser()
parser.add_argument("file", help = "allows to add the file path", type=str)
args = parser.parse_args()


#-------------- Non FM demodulated data --------------#

#-------------- FM demodulated data --------------#

fs, Y_decode = wavfile.read(args.file) #opening the wav file
temp = Y_decode(:, 2).'
