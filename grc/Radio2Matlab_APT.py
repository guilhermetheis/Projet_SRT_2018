#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Receiver for NOAA APT
# Author: Guilherme Theis and Sébastien Descombes
# Description: This is a receiver block for NOAA APT images the rest of the processing is done by another software
# Generated: Fri Dec  7 11:04:04 2018
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class Radio2Matlab_APT(grc_wxgui.top_block_gui):

    def __init__(self, antenna='RX1', audioRate=192000, bandwidth=40E3, centerFrequency=137.1E6, gain=10, outputFile="/results/output.data", samplingRate=1000000):
        grc_wxgui.top_block_gui.__init__(self, title="Receiver for NOAA APT")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.antenna = antenna
        self.audioRate = audioRate
        self.bandwidth = bandwidth
        self.centerFrequency = centerFrequency
        self.gain = gain
        self.outputFile = outputFile
        self.samplingRate = samplingRate

        ##################################################
        # Blocks
        ##################################################
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "FMSignal")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "FMWaterfall")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "DemodSignal")
        self.Add(self.notebook_0)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(1).GetWin(),
        	baseband_freq=centerFrequency,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samplingRate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0_1 = fftsink2.fft_sink_f(
        	self.notebook_0.GetPage(2).GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=audioRate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='AudioOutput',
        	peak_hold=False,
        )
        self.notebook_0.GetPage(2).Add(self.wxgui_fftsink2_0_1.win)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=centerFrequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samplingRate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Apr\xc3\xa8s filtre',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=centerFrequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samplingRate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Avant filtre',
        	peak_hold=False,
        	win=window.hanning,
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_0.win)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samplingRate)
        self.uhd_usrp_source_0.set_center_freq(centerFrequency, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna(antenna, 0)
        self.uhd_usrp_source_0.set_bandwidth(bandwidth, 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=192,
                decimation=48,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=audioRate,
                decimation=samplingRate,
                taps=None,
                fractional_bw=None,
        )
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/net/e/gtheis/code/Projet_SRT_2018/outputfiles/output', 1, audioRate, 8)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/net/e/gtheis/code/Projet_SRT_2018/outputfiles/outputfile_complex', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, samplingRate, centerFrequency-bandwidth/2, centerFrequency+bandwidth/2, bandwidth/2/6, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=audioRate,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.band_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.wxgui_fftsink2_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_waterfallsink2_0, 0))

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.uhd_usrp_source_0.set_antenna(self.antenna, 0)

    def get_audioRate(self):
        return self.audioRate

    def set_audioRate(self, audioRate):
        self.audioRate = audioRate
        self.wxgui_fftsink2_0_1.set_sample_rate(self.audioRate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 0)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samplingRate, self.centerFrequency-self.bandwidth/2, self.centerFrequency+self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))

    def get_centerFrequency(self):
        return self.centerFrequency

    def set_centerFrequency(self, centerFrequency):
        self.centerFrequency = centerFrequency
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.centerFrequency)
        self.wxgui_fftsink2_0_0.set_baseband_freq(self.centerFrequency)
        self.wxgui_fftsink2_0.set_baseband_freq(self.centerFrequency)
        self.uhd_usrp_source_0.set_center_freq(self.centerFrequency, 0)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samplingRate, self.centerFrequency-self.bandwidth/2, self.centerFrequency+self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)


    def get_outputFile(self):
        return self.outputFile

    def set_outputFile(self, outputFile):
        self.outputFile = outputFile

    def get_samplingRate(self):
        return self.samplingRate

    def set_samplingRate(self, samplingRate):
        self.samplingRate = samplingRate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samplingRate)
        self.wxgui_fftsink2_0_0.set_sample_rate(self.samplingRate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samplingRate)
        self.uhd_usrp_source_0.set_samp_rate(self.samplingRate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samplingRate, self.centerFrequency-self.bandwidth/2, self.centerFrequency+self.bandwidth/2, self.bandwidth/2/6, firdes.WIN_HAMMING, 6.76))


def argument_parser():
    description = 'This is a receiver block for NOAA APT images the rest of the processing is done by another software'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "-a", "--antenna", dest="antenna", type="string", default='RX1',
        help="Set antennaUsed [default=%default]")
    parser.add_option(
        "-r", "--audioRate", dest="audioRate", type="eng_float", default=eng_notation.num_to_str(192000),
        help="Set audio_rate [default=%default]")
    parser.add_option(
        "-b", "--bandwidth", dest="bandwidth", type="eng_float", default=eng_notation.num_to_str(40E3),
        help="Set bw [default=%default]")
    parser.add_option(
        "-f", "--centerFrequency", dest="centerFrequency", type="eng_float", default=eng_notation.num_to_str(137.1E6),
        help="Set center_freq [default=%default]")
    parser.add_option(
        "-g", "--gain", dest="gain", type="intx", default=10,
        help="Set radioGain [default=%default]")
    parser.add_option(
        "-o", "--outputFile", dest="outputFile", type="string", default="/results/output.data",
        help="Set file [default=%default]")
    parser.add_option(
        "-s", "--samplingRate", dest="samplingRate", type="intx", default=1000000,
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=Radio2Matlab_APT, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(antenna=options.antenna, audioRate=options.audioRate, bandwidth=options.bandwidth, centerFrequency=options.centerFrequency, gain=options.gain, outputFile=options.outputFile, samplingRate=options.samplingRate)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
