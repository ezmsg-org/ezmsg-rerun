import ezmsg.core as ez
import rerun as rr
import numpy as np
from ezmsg.sigproc.synth import EEGSynth
from ezmsg.rerun import Rerun
from ezmsg.util.debuglog import DebugLog


class Test(ez.Collection):
    VIZ = Rerun()
    SOURCE = EEGSynth()

    def network(self):
        return ((self.SOURCE.OUTPUT_SIGNAL, self.VIZ.INPUT_SIGNAL),)

    def process_components(self):
        return (
            self.VIZ,
            self.SOURCE,
        )


if __name__ == "__main__":
    ez.run(TEST=Test())
    # rr.init("rerun_example_send_columns", spawn=True)
    #
    # times = np.arange(0, 64)
    # rr.send_columns(
    #     "scalars",
    #     times=[rr.TimeSequenceColumn("step", np.arange(0, 64))],
    #     components=[rr.components.ScalarBatch(np.sin(times / 10.0))],
    # )
