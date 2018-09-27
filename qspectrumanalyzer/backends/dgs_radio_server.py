import shlex
import os
import json
from Qt import QtCore

from qspectrumanalyzer import subproc
from qspectrumanalyzer.backends import BaseInfo, BasePowerThread


class Info(BaseInfo):
    pass


class PowerThread(BasePowerThread):

    def setup(self, start_freq, stop_freq, bin_size, interval=10.0, gain=-1, ppm=0, crop=0,
              single_shot=False, device="", sample_rate=2560000, bandwidth=0, lnb_lo=0):
        self.params = {
            "hops": 0
        }
        self.databuffer = {}

    def process_start(self):
        if not self.process and self.params:
            settings = QtCore.QSettings()
            cmdline = shlex.split(os.path.join(os.getcwd(), settings.value("executable", "dgs_radio_server")))
            cmdline.extend([
                "-s", "{}".format("tcp://127.0.0.1:5556")
            ])
            print('Starting backend:')
            print(' '.join(cmdline))
            print()
            self.process = subproc.Popen(cmdline, stdout=subproc.PIPE,
                                         universal_newlines=True, console=False)

    def parse_output(self, line):

        data = json.loads(line)
        self.databuffer = {"timestamp": data['msec'],
                           "x": data['fftData'],
                           "y": data['fftFreqData']}

        self.data_storage.update(self.databuffer)