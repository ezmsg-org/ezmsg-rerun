import typing

import ezmsg.core as ez
from ezmsg.util.messages.axisarray import AxisArray

import rerun as rr
import rerun.blueprint as rrb


class RerunSettings(ez.Settings):
    name: str = "EzRerun"
    spawn: bool = True
    channelize: bool = True
    base_entity_path: str = "axisarray"
    time_dim: typing.Union[str, int] = "time"
    window_size: int = 5


class RerunState(ez.State):
    num_channels: typing.Optional[int] = None


class Rerun(ez.Unit):
    SETTINGS = RerunSettings
    STATE = RerunState

    INPUT_SIGNAL = ez.InputStream(AxisArray)

    async def initialize(self) -> None:
        rr.init(
            self.SETTINGS.name,
            spawn=self.SETTINGS.spawn,
        )

    @ez.subscriber(INPUT_SIGNAL)
    async def on_aa(self, message: AxisArray):
        time_arr = message.ax(self.SETTINGS.time_dim).values
        with message.view2d(self.SETTINGS.time_dim) as data:
            if (
                self.STATE.num_channels is None
                or self.STATE.num_channels != data.shape[-1]
            ):
                if self.SETTINGS.channelize is True:
                    blueprint = rrb.Grid(
                        contents=[
                            rrb.TimeSeriesView(
                                origin=f"{self.SETTINGS.base_entity_path}/{i}",
                                name=f"Channel {i}",
                                time_ranges=[
                                    rrb.VisibleTimeRange(
                                        "s",
                                        start=rrb.TimeRangeBoundary.cursor_relative(
                                            seconds=-self.SETTINGS.window_size
                                        ),
                                        end=rrb.TimeRangeBoundary.cursor_relative(),
                                    )
                                ],
                                plot_legend=rrb.PlotLegend(visible=False),
                            )
                            for i in range(data.shape[-1])
                        ]
                    )
                else:
                    blueprint = rrb.TimeSeriesView(
                        origin=f"{self.SETTINGS.base_entity_path}/",
                        time_ranges=[
                            rrb.VisibleTimeRange(
                                "s",
                                start=rrb.TimeRangeBoundary.cursor_relative(
                                    seconds=-self.SETTINGS.window_size
                                ),
                                end=rrb.TimeRangeBoundary.cursor_relative(),
                            )
                        ],
                        plot_legend=rrb.PlotLegend(visible=False),
                    )
                rr.send_blueprint(blueprint)
                self.STATE.num_channels = data.shape[-1]

            for i in range(data.shape[-1]):
                rr.send_columns(
                    f"{self.SETTINGS.base_entity_path}/{i}",
                    times=[rr.TimeSecondsColumn("s", time_arr)],
                    components=[rr.components.ScalarBatch(data[:, i])],
                )
