from support.Tables import *
from support.ADSR import Envelope
from support.osc import Oscillator


class Voice:

    _tune_freq: float = 0.0;

    def __init__(self, sampling_frequecy: int = 44100) -> None:
        self._osc: Oscillator = Oscillator(sampling_frequecy)
        self._adsr: Envelope = Envelope(sampling_frequecy)

    def note_on(self, freq: float) -> None:
        self._osc.frequency = freq + self._tune_freq
        self._adsr.trigger_key()

    def note_off(self) -> None:
        self._adsr.release_key()

    def change_table(self, table:TABLE_INT) -> None:
        self._osc.change_table(table)
    
    def sync(self) -> None:
        self._osc.sync()

    def update_adsr(self, attack: int|None = None, decay: int|None = None, sustain: float|None = None, release: int|None = None) -> None:
        self._adsr.attack   = attack    if attack else self._adsr.attack
        self._adsr.decay    = decay     if decay else self._adsr.decay
        self._adsr.sustain  = sustain   if sustain else self._adsr.sustain
        self._adsr.release  = release   if release else self._adsr.release

    def tune(self, tune_freq: float = 0.0) -> None:
        self._tune_freq = tune_freq

    def gen_frame(self, frame_len: int) -> TABLE:
        adsr: TABLE = self._adsr.gen_frame(frame_len)
        osc: TABLE = self._osc.gen_frame(frame_len)
        out: TABLE = []
        for i in range(frame_len):
            out.append(adsr[i]*osc[i])
        return out

    def is_active(self) -> bool:
        return self._adsr.is_active()


def main() -> None:
    import matplotlib.pyplot as plt
    v = Voice()
    sr = 44100
    def gen_note(freq: float, sync:bool=False):
        f = v.gen_frame(int(sr*0.1))
        v.note_on(freq)
        v.sync() if sync else None
        f.extend(v.gen_frame(30870))
        v.note_off()
        f.extend(v.gen_frame(22050))
        _, ax = plt.subplots()
        _ = ax.plot(f)
        plt.show()
    gen_note(440)

    v.change_table(TRIANGLE)
    gen_note(30, True)
    



if __name__ == "__main__":
    main()
