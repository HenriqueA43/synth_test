from support.Tables import *

class Oscillator:

    _sample_frequency: int = 44100
    _table:list[int] = SINE
    _tab_len: int = len(_table)
    _kincr_const_calc: float = _tab_len/_sample_frequency
    _freq: float|int = 440.0
    _targ_freq: float|int = 440
    _kincr: float = 0.0
    _curidx: float = 0.0

    def _update_kincr(self) -> None:
        self._kincr = self._tab_len*self._freq/self._sample_frequency

    def __init__(self, sample_freq: int|float = 44100, wavetable:list[int] = SINE, frequency: float|int = 440):  
        self.sample_frequency = sample_freq
        self._table = wavetable
        self.frequency = frequency
        self._update_kincr()

    @property
    def sample_frequency(self) -> int|float:
        return self._sample_frequency

    @sample_frequency.setter
    def sample_frequency(self, val: int|float) -> None:
        if type(val) not in [int, float]:
            raise TypeError
        val = int(val)
        self._sample_frequency = max(val, 0)
        self._update_kincr()

    @property
    def frequency(self) -> int|float:
        return self._freq

    @frequency.setter
    def frequency(self, val: float|int) -> None:
        self._targ_freq = min(max(0, val), self._sample_frequency/2)

    def change_table(self,wavetable: list[int]) -> None:
        L: int = len(wavetable)
        if L:
            self._tab_len = L
            self._table = wavetable
            self._update_kincr()

    def sync(self) -> None: 
        self._curidx = 0
        self._freq = self._targ_freq
        self._update_kincr()



    def gen_frame(self, samples: int) -> list[float]:
        delta_freq = 0.0
        if self._targ_freq != self._freq:
            delta_freq = (self._targ_freq-self._freq)/samples
        out: list[float] = []
        for i in range(samples):
            if delta_freq:
                self._freq += delta_freq
                self._update_kincr()
            next_idx = int(self._curidx+1)%(self._tab_len - 1)
            remainder = self._curidx%1
            cur_idx = int(self._curidx)
            out.append( (1-remainder)*self._table[cur_idx] + remainder*self._table[next_idx] )
            self._curidx = (self._curidx + self._kincr)%(self._tab_len-1)
        return out


def _test_frequency() -> None:
    sample_freq = 44100
    osc = Oscillator(sample_freq=sample_freq) 
    osc.frequency = -1 
    assert osc._targ_freq == 0, f"Sample frequency not being clamped to 0! current target frequency: {osc._targ_freq}"
    osc.sample_frequency = sample_freq
    osc.frequency = sample_freq
    assert osc._targ_freq == sample_freq/2, "Sample frequency not being clamped to nyquist!"

def _test_table() -> None:
    osc = Oscillator()
    ref_table = SINE
    osc.change_table(ref_table)
    osc.change_table([])
    assert osc._table == ref_table, "Setting table to nothing is not ignored!"

def _test_sync() -> None:
    osc = Oscillator()
    osc.gen_frame(1)
    curphase = osc._curidx
    assert curphase != 0, "Oscillator is not incrementing phase"
    osc.sync()
    assert osc._curidx == 0, "Sync does not reset phase to 0"
    



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # unit tests
    _test_sync()
    _test_table()
    _test_frequency()
    print(" ---> All Oscillator Unit tests Passed! <--- ")


    def plot_simple(signal : list[float|int], show: bool = False) -> None:
        fig, ax = plt.subplots()  # pyright: ignore[reportUnknownMemberType, reportUnusedVariable]
        _ = ax.plot(signal)  # pyright: ignore[reportUnknownMemberType]
        plt.show() if show else None # pyright: ignore[reportUnknownMemberType]
    
    o = Oscillator()
    plot_simple(o.gen_frame(512))
    o.frequency = 110
    o.sync()
    o.frequency = 880
    o.change_table(TRIANGLE)
    out = o.gen_frame(256)
    out.extend(o.gen_frame(256))
    plot_simple(out, show = True)




