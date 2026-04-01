#! /usr/bin/env python
import matplotlib.pyplot as plt
from support import wavetables as wav
import numpy as np

def main():
    w = wav.Triangle()
    fft = np.abs(np.fft.fft(w.table))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(fft)
    plt.show()

def test():
    import numpy as np
    import matplotlib.pyplot as plt
    from support.wavetables.triangle import Triangle
    t = Triangle()
    wave = np.array(t.table, dtype=np.float64)
    n = len(wave)
    sr = 44100  # sample rate
    freqs = np.fft.rfftfreq(n, 1/sr)
    fft = np.fft.rfft(wave)
    cutoffs = [2000, 4000, 10000]
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes[0, 0].plot(wave)
    axes[0, 0].set_title('Original')
    for ax, cutoff in zip(axes.flat[1:], cutoffs):
        filtered = fft.copy()
        filtered[freqs > cutoff] = 0
        result = np.fft.irfft(filtered, n)
        ax.plot(result)
        ax.set_title(f'Band-limited to {cutoff} Hz')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # main()
    test()
