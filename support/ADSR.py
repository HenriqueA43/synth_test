from dataclasses import dataclass
from enum import StrEnum, auto


class State(StrEnum):
    IDLE    = auto()
    ATTACK  = auto()
    DECAY   = auto()
    SUSTAIN = auto()
    RELEASE = auto()


@dataclass
class Envelope:

    _sampling_rate: int     = 44100

    _attack_len_ms: int     = 100
    _attack_inc:    float   = 1000/(_sampling_rate*_attack_len_ms)
    _decay_len_ms:  int     = 200
    _decay_inc:     float   = -1000/(_sampling_rate*_decay_len_ms)
    _sustain_amm:   float   = 0.5
    _release_len_ms:int     = 500
    _release_inc:   float   = -1000/(_sampling_rate*_release_len_ms)
    _state: State = State.IDLE
    _curval:        float   = 0.0
    
    def __post_init__(self):
        pass

    @property
    def attack(self) -> int:
        "Attack len in ms"
        return self._attack_len_ms
    @attack.setter
    def attack(self, val: int):
        self._attack_len_ms = max(val, 20)
        self._attack_inc = 1000/(self._sampling_rate*self._attack_len_ms)
   
    @property
    def decay(self) -> int:
        return self._decay_len_ms
    @decay.setter
    def decay(self, val: int) -> None:
        self._decay_len_ms = max(val, 100)
        self._decay_inc = -1000/(self._sampling_rate*self._decay_len_ms)

    @property
    def sustain(self) -> float:
        return self._sustain_amm
    @sustain.setter
    def sustain(self, val:float) -> None:
        self._sustain_amm = min(max(val, 0),1)

    @property
    def release(self) -> int:
        return self._release_len_ms
    @release.setter
    def release(self, val: int) -> None:
        self._release_len_ms = max(val, 0)
        self._release_inc = -1000/(self._sampling_rate*self._release_len_ms)

    def trigger_key(self) -> None:
        self._state = State.ATTACK

    def release_key(self) -> None:
        self._state = State.RELEASE

    def _calc_envelope_value(self) -> float:
        out: float = self._curval
        match self._state:

            case State.IDLE:
                return 0.0

            case State.ATTACK:
                self._curval+=self._attack_inc
                if self._curval >= 1:
                    self._curval = 1.0
                    self._state = State.DECAY

            case State.DECAY:
                self._curval+=self._decay_inc
                if self._curval <= self._sustain_amm:
                    self._curval = self._sustain_amm
                    self._state = State.SUSTAIN

            case State.SUSTAIN:
                return self._sustain_amm

            case State.RELEASE:
                self._curval+=self._release_inc
                if self._curval <= 0:
                    self._curval = 0
                    self._state = State.IDLE
        return out

    def gen_frame(self, frame_len: int) -> list[float]:
        out: list[float] = []
        for _ in range(frame_len):
            out.append(self._calc_envelope_value())
        return out

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    myADSR = Envelope()
    fig, ax = plt.subplots()
    sr = myADSR._sampling_rate
    aL = int(myADSR.attack/1000*sr)
    dL = int((1-myADSR.sustain)*myADSR.decay/1000*sr )
    sL = int(0.5 * sr) 
    full = myADSR.gen_frame(int(0.1*sr))
    myADSR.trigger_key()
    full.extend(myADSR.gen_frame(aL+dL+sL))
    myADSR.release_key()
    rL = int(myADSR.sustain*myADSR.release/1000*sr)
    full.extend(myADSR.gen_frame(rL+int(0.1*sr)))
    # full.extend(myADSR.gen_frame(rL))

    print(f"{aL = }, {dL = }, {sL = }, {rL = }")


    ax.plot(full)
    plt.show()

