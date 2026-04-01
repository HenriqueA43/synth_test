from support.Wavetables import Wavetables as wav 

class Oscillator:

    _sample_frequency: int|float = 44100
    _table:list[int] = wav.SINE 
    _tab_len: int = len(_table)
    _kincr_const_calc: float = _tab_len/_sample_frequency
    _freq: float|int = 440.0
    _kincr: float = 0.0
    _curidx: float = 0.0

    def _update_kincr(self) -> None:
        self._kincr = self._tab_len*self._freq/self._sample_frequency

    def __init__(self, sample_freq: int|float = 44100, wavetable:list[int] = wav.SINE, frequency: float|int = 440):  
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
        self._freq = min(max(0, val), self._sample_frequency/2)
        self._update_kincr()

    def change_table(self,wavetable: list[int]) -> None:
        L: int = len(wavetable)
        if L:
            self._tab_len = L
            self._table = wavetable
        self._update_kincr()

    def gen_frame(self, samples: int) -> list[float]:
        out: list[float] = []
        for i in range(samples):
            next_idx = int(self._curidx+1)%(self._tab_len - 1)
            remainder = self._curidx%1
            cur_idx = int(self._curidx)
            out.append( (1-remainder)*self._table[cur_idx] + remainder*self._table[next_idx] )
            self._curidx = (self._curidx + self._kincr)%(self._tab_len-1)
        return out

