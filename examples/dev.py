import ezmsg.core as ez
from ezmsg.sigproc.synth import EEGSynth
from ezmsg.rerun import Rerun, RerunSettings


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
    settings = RerunSettings(
        name="EEG Synth",
        channelize=False,
        base_entity_path="eeg",
    )
    collection = Test(settings=settings)
    ez.run(EEG=collection)
