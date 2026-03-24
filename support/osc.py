from support import wavetables as wav 


class Oscillator:

    _sample_frequency: int = 44100

    def __init__(self, *args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        if 'sample_frequency' in kwargs.keys():
            self.sample_frequency = kwargs['sample_frequency']
        self.osc_type = wav.Triangle()

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


    
