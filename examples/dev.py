import ezmsg.core as ez
from ezmsg.sigproc.synth import EEGSynth
from ezmsg.rerun import Rerun, RerunSettings


class Test(ez.Collection):
    VIZ = Rerun()
    SOURCE = EEGSynth()

    def configure(self) -> None:
        self.VIZ.apply_settings(
            RerunSettings(
                name="EEG Synth",
                channelize=False,
                base_entity_path="eeg",
            )
        )

    def network(self):
        return ((self.SOURCE.OUTPUT_SIGNAL, self.VIZ.INPUT_SIGNAL),)

    def process_components(self):
        return (
            self.VIZ,
            self.SOURCE,
        )


if __name__ == "__main__":
    ez.run(TEST=Test())
