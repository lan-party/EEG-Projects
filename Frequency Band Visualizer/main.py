import sys
from PyQt5 import QtWidgets, QtSvg, QtCore
import time
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations
import numpy as np

# shape_colors = ["ff6961", "ffb480", "f8f38d", "42d6a4", "08cad1", "59adf6", "9d94ff", "c780e8"]
shape_colors = ["ffb480"]*8

svg_str = """<?xml version="1.0" standalone="no"?>
<svg width="576pt"
    height="576pt"
    viewBox="0 0 576 576">
<defs/>
<path id="shape0" transform="translate(222.82182774, 327.41734239)" fill="#"""+shape_colors[0]+"""" fill-rule="evenodd" d="M0 32.2688C11.1272 21.1416 22.1616 13.1672 33.1034 8.34539C44.0451 3.52361 55.8214 0.741812 68.4322 0L68.154 149.104C68.154 149.104 45.436 110.159 0 32.2688Z"/>
    <path id="shape1" transform="translate(174.97494339, 224.49090511)" fill="#"""+shape_colors[1]+"""" fill-rule="evenodd" d="M116.001 25.3143C102.092 24.5725 90.3156 21.2344 80.6721 15.2999C71.0285 9.36538 63.9813 4.26542 59.5304 0L0 52.8541L40.6142 123.234C53.4105 111.179 66.2067 102.834 79.003 98.1974C91.7993 93.5611 104.132 90.6865 116.001 89.5738C116.001 89.5738 116.001 68.154 116.001 25.3143Z"/>
    <path id="shape2" transform="translate(110.43728541, 166.90773614)" fill="#"""+shape_colors[2]+"""" fill-rule="evenodd" d="M115.166 47.0123L57.8613 98.7537L0 0L98.4756 0.27818C98.4756 9.55083 100.145 17.8962 103.483 25.3143C108.49 36.4415 108.49 36.4415 115.166 47.0123Z"/>
    <path id="shape3" transform="translate(221.43092994, 166.90773614)" fill="#"""+shape_colors[3]+"""" fill-rule="evenodd" d="M69.5449 0.556359L0 0C0.741812 16.8762 7.23267 31.8979 19.4726 45.0651C31.7125 58.2323 48.4032 66.3922 69.5449 69.5449C69.5449 69.5449 69.5449 46.5487 69.5449 0.556359Z"/>
    <path id="shape0" transform="matrix(-1.0000000075 0 0 0.99999999335 372.30428407 327.60076944)" fill="#"""+shape_colors[4]+"""" fill-rule="evenodd" d="M0 32.2688C11.1272 21.1416 22.1616 13.1672 33.1034 8.34539C44.0451 3.52361 55.8214 0.741812 68.4322 0L68.154 149.104C68.154 149.104 45.436 110.159 0 32.2688Z"/>
    <path id="shape1" transform="matrix(-1.0000000075 0 0 0.99999999335 420.15116878 224.67433285)" fill="#"""+shape_colors[5]+"""" fill-rule="evenodd" d="M116.001 25.3143C102.092 24.5725 90.3156 21.2344 80.6721 15.2999C71.0285 9.36538 63.9813 4.26542 59.5304 0L0 52.8541L40.6142 123.234C53.4105 111.179 66.2067 102.834 79.003 98.1974C91.7993 93.5611 104.132 90.6865 116.001 89.5738C116.001 89.5738 116.001 68.154 116.001 25.3143Z"/>
    <path id="shape2" transform="matrix(-1.0000000075 0 0 0.99999999335 484.68882725 167.09116426)" fill="#"""+shape_colors[6]+"""" fill-rule="evenodd" d="M115.166 47.0123L57.8613 98.7537L0 0L98.4756 0.27818C98.4756 9.55083 100.145 17.8962 103.483 25.3143C108.49 36.4415 108.49 36.4415 115.166 47.0123Z"/>
    <path id="shape3" transform="matrix(-1.0000000075 0 0 0.99999999335 373.69518188 167.09116426)" fill="#"""+shape_colors[7]+"""" fill-rule="evenodd" d="M69.5449 0.556359L0 0C0.741812 16.8762 7.23267 31.8979 19.4726 45.0651C31.7125 58.2323 48.4032 66.3922 69.5449 69.5449C69.5449 69.5449 69.5449 46.5487 69.5449 0.556359Z"/>
</svg>
"""
svg_str_copy = svg_str

svg_bytes = bytearray(svg_str, encoding='utf-8')

start_stream = False
stream_running = False
stop_stream = False
freq_bands = [[0,4],[4,7],[8,12],[12,30],[30,100]]
current_freq_band = 2

color_count = 30

freq_band_colors = [np.array(
        [np.rint(np.linspace(255, 255, color_count)), np.rint(np.linspace(136, 161, color_count)), np.rint(np.linspace(136, 0, color_count))]).T,
     np.array(
        [np.rint(np.linspace(255, 177, color_count)), np.rint(np.linspace(246, 255, color_count)), np.rint(np.linspace(136, 0, color_count))]).T,
     np.array(
        [np.rint(np.linspace(137, 0, color_count)), np.rint(np.linspace(255, 223, color_count)), np.rint(np.linspace(173, 255, color_count))]).T,
     np.array(
        [np.rint(np.linspace(135, 57, color_count)), np.rint(np.linspace(208, 0, color_count)), np.rint(np.linspace(255, 255, color_count))]).T,
     np.array(
        [np.rint(np.linspace(232, 255, color_count)), np.rint(np.linspace(144, 0, color_count)), np.rint(np.linspace(255, 138, color_count))]).T]
# freq_band_colors = [np.array(
#         [np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count))]).T,np.array(
#         [np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count))]).T,np.array(
#         [np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count))]).T,np.array(
#         [np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count))]).T,np.array(
#         [np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count)), np.rint(np.linspace(0, 255, color_count))]).T]

class bgListener(QtCore.QThread):
    band_power = QtCore.pyqtSignal(list)

    def run(self):
        global start_stream
        global stream_running
        global stop_stream
        global freq_bands
        global current_freq_band
        global svg_str

        BoardShim.enable_dev_board_logger()
        params = BrainFlowInputParams()
        params.serial_port = 'COM3'
        board = BoardShim(BoardIds.CYTON_BOARD.value, params)
        channels = {}

        while True:
            try:
                if start_stream:
                    board.prepare_session()
                    board.start_stream()
                    time.sleep(3)
                    start_stream = False
                    stream_running = True

                if stop_stream:
                    board.stop_stream()
                    board.release_session()
                    stop_stream = False

                if stream_running:
                    data = board.get_board_data()

                    board_descr = BoardShim.get_board_descr(BoardIds.CYTON_BOARD.value)
                    sampling_rate = int(board_descr['sampling_rate'])
                    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
                    detrend_data = data
                    channels_copy = {}
                    if channels != {}:
                        channels_copy = channels
                    channels = {}
                    channel_bands = []
                    for eeg_channel in board_descr['eeg_channels']:
                        DataFilter.detrend(detrend_data[eeg_channel], DetrendOperations.LINEAR.value)
                        psd = DataFilter.get_psd_welch(detrend_data[eeg_channel], nfft, nfft // 2, sampling_rate,
                                                       WindowOperations.BLACKMAN_HARRIS.value)
                        channels[eeg_channel] = []
                        current_index = 0
                        for freq_band in freq_bands:
                            if channels_copy != {}:
                                power = round((round(DataFilter.get_band_power(psd, freq_band[0], freq_band[1]), 2) + channels_copy[eeg_channel][current_index]) / 2, 2)
                            else:
                                power = round(DataFilter.get_band_power(psd, freq_band[0], freq_band[1]), 2)
                            power = (color_count-1 if power >= color_count else power)
                            channels[eeg_channel].append(power)
                            current_index += 1

                        channel_bands.append(channels[eeg_channel][current_freq_band])

                    self.band_power.emit(channel_bands)

                    time.sleep(2)
                else:
                    if svg_str.count("42d6a4") < 8:
                        svg_str = svg_str.replace("ffb480", "42d6a4", 1)
                    else:
                        svg_str = svg_str.replace("42d6a4", "ffb480")
                    svg_bytes = bytearray(svg_str, encoding='utf-8')
                    self.band_power.emit([svg_bytes])

                    time.sleep(1)
            except Exception as e:
                print("ERR:",e)
            time.sleep(0.1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setGeometry(416, 66, 768, 768)
        self.setFixedSize(768, 768)
        self.setStyleSheet("background-color: #111111;")
        self.setWindowTitle("EEG Frequency Band Visualizer")

        self.svgWidget = QtSvg.QSvgWidget(self)
        self.svgWidget.renderer().load(svg_bytes)
        self.svgWidget.setMinimumSize(768, 768)

        self.streamAction = QtWidgets.QAction('&Start Stream', self)
        self.streamAction.triggered.connect(self.startStream)
        self.deltaSelectAction = QtWidgets.QAction('&Delta (0-4 Hz)', self)
        self.deltaSelectAction.triggered.connect(self.deltaSelect)
        self.thetaSelectAction = QtWidgets.QAction('&Theta (4-7 Hz)', self)
        self.thetaSelectAction.triggered.connect(self.thetaSelect)
        self.alphaSelectAction = QtWidgets.QAction('&Alpha (8-12 Hz)', self)
        self.alphaSelectAction.triggered.connect(self.alphaSelect)
        self.betaSelectAction = QtWidgets.QAction('&Beta (12-30 Hz)', self)
        self.betaSelectAction.triggered.connect(self.betaSelect)
        self.gammaSelectAction = QtWidgets.QAction('&Gamma (30+ Hz)', self)
        self.gammaSelectAction.triggered.connect(self.gammaSelect)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.resize(768, 21)
        self.menuBar.setStyleSheet("background-color: #EEEEEE;")
        self.freqBandMenu = self.menuBar.addMenu('&Frequency Band')
        self.freqBandMenu.addAction(self.deltaSelectAction)
        self.freqBandMenu.addAction(self.thetaSelectAction)
        self.freqBandMenu.addAction(self.alphaSelectAction)
        self.freqBandMenu.addAction(self.betaSelectAction)
        self.freqBandMenu.addAction(self.gammaSelectAction)
        self.menuBar.addAction(self.streamAction)

        self.bg = bgListener()
        self.bg.start()
        self.bg.band_power.connect(self.updateTiles)

    def startStream(self, event):
        global start_stream
        global stream_running
        global stop_stream

        if stream_running:
            stop_stream = True
            self.streamAction.setText("Start Stream")
        else:
            start_stream = True
            self.streamAction.setText("Stop Stream")

    def deltaSelect(self, event):
        global current_freq_band
        print("delta")
        current_freq_band = 0

    def thetaSelect(self, event):
        global current_freq_band
        print("theta")
        current_freq_band = 1

    def alphaSelect(self, event):
        global current_freq_band
        print("alpha")
        current_freq_band = 2

    def betaSelect(self, event):
        global current_freq_band
        print("beta")
        current_freq_band = 3

    def gammaSelect(self, event):
        global current_freq_band
        print("gamma")
        current_freq_band = 4

    def updateTiles(self, band_power):
        global stream_running
        global freq_band_colors
        global current_freq_band
        global svg_str_copy

        if stream_running:
            print(band_power)
            try:
                svg_str_split = svg_str_copy.split("#ffb480")
                svg_str = ""
                electrode_locations = [6,4,2,0,7,5,3,2]
                for a in range(0,8):
                    color = "rgb(" + ",".join([str(int(i)) for i in freq_band_colors[current_freq_band][int(band_power[electrode_locations[a]])]]) + ")"
                    svg_str += svg_str_split[a] + color
                svg_str += svg_str_split[8]
                svg_bytes = bytearray(svg_str, encoding='utf-8')
                self.svgWidget.renderer().load(svg_bytes)
            except Exception as e:
                print("ERR:",e)

        else:
            self.svgWidget.renderer().load(band_power[0])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
