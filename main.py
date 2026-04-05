#! /usr/bin/env python
import matplotlib.pyplot as plt
from support.Tables import *
from support.osc import Oscillator
from support.ADSR import Envelope
from support.voice import Voice


def test_osc():

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


def test_key() -> None:
    import keyboard
    pressed: set[keyboard._Key]  = set()
    v = Voice()






if __name__ == "__main__":
    test_osc()
