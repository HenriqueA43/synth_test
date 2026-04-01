from support import Wavetables as wav 

class Oscillator:

    _sample_frequency: int = 44100
    _osc_type = wav.SINE 

    def __init__(self, sample_freq: 44100, ):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
            self.sample_frequency = kwargs['']
    @property
    def sample_frequency(self) -> int:
        return self._sample_frequency

    @sample_frequency.setter
    def sample_frequency(self, val: int) -> None:
        if type(val) not in [int, float]:
            raise TypeError
        val = int(val)
        if val < 0:
            self._sample_frequency = 0
        else:
            self._sample_frequency = val


    
