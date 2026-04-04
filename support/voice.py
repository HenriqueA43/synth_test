from support.Tables import *
from support.ADSR import Envelope
from support.osc import Oscillator


class Voice:

    def __init__(self, sampling_frequecy: int = 44100) -> None:
        self._osc = Oscillator(sampling_frequecy)
        self._adsr = Envelope(sampling_frequecy)

    def note_on(self, freq: float) -> None:
        self._osc.frequency = freq
        self._adsr.trigger_key()

    def note_off(self) -> None:
        self._adsr.release_key()

    def change_table(self, table:list[int]) -> None:
        self._osc.change_table(table)
    
    def sync(self) -> None:
        self._osc.sync()

    def gen_frame(self, frame_len: int) -> list[float]:
        adsr = self._adsr.gen_frame(frame_len)
        osc = self._osc.gen_frame(frame_len)
        out: list[float] = []
        for i in range(frame_len):
            out.append(adsr[i]*osc[i])
        return out


def main() -> None:
    import matplotlib.pyplot as plt
    v = Voice()
    sr = 44100
    def gen_note(freq: float, sync=False):
        f = v.gen_frame(int(sr*0.1))
        print(v._osc.frequency)
        v.note_on(freq)
        print(v._osc.frequency)
        v.sync() if sync else None
        print(v._osc.frequency)
        f.extend(v.gen_frame(30870))
        v.note_off()
        f.extend(v.gen_frame(22050))
        fig, ax = plt.subplots()
        ax.plot(f)
        plt.show()
    gen_note(440)

    v.change_table(TRIANGLE)
    gen_note(30, True)
    



if __name__ == "__main__":
    main()
