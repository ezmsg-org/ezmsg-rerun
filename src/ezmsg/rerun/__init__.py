import asyncio
import ezmsg.core as ez
import rerun as rr
import rerun.blueprint as rrb
import numpy as np
from ezmsg.util.messages.axisarray import AxisArray


class Rerun(ez.Unit):
    INPUT_SIGNAL = ez.InputStream(AxisArray)

    async def initialize(self) -> None:
        rr.init("rerun_example_send_columns", spawn=True)
        self.offset = None
        self.num_samps = 0

    @ez.subscriber(INPUT_SIGNAL)
    async def on_aa(self, message: AxisArray):
        time_arr = message.ax("time").values
        data = message.data
        for i in range(data.shape[1]):
            rr.send_columns(
                f"eeg/{i}",
                times=[rr.TimeSecondsColumn("s", time_arr)],
                components=[rr.components.ScalarBatch(data[:, i])],
            )
