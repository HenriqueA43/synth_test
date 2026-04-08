import collections
from collections.abc import Generator
from hmac import new
from random import sample

import matplotlib
import matplotlib.animation as anim 
import matplotlib.pyplot as plt 
from matplotlib.backend_bases import KeyEvent
from matplotlib.lines import Line2D

from support.Tables import SINE, TRIANGLE
from support.voice import Voice


class Oscilloscope:

    def __init__(
            self,
            ax: plt.Axes,
            voice: Voice,
            frames: int = 8,
            samples_per_frame: int = 2205,
    ) -> None:
        self.ax = ax
        self.voice = voice
        self.frames = frames
        self.samples_per_frame = samples_per_frame
        self.buffer: collections.deque[float] = collections.deque(
            maxlen=frames * samples_per_frame
        )
        self.buffer.extend([0]*frames * samples_per_frame)

        self.line = Line2D([], [], linewidth=1)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-35000, 35000)
        self.ax.set_xlim(0,frames*samples_per_frame)
        self._update_title()

    def update(self, _) -> tuple[Line2D]:
        new_samples = self.voice.gen_frame(self.samples_per_frame)
        self.buffer.extend(new_samples)
        # print(list(self.buffer))
        self.line.set_data(range(len(self.buffer)), list(self.buffer))
        self._update_title()
        return (self.line,)

    def _update_title(self) -> None:
        freq = self.voice._osc.frequency
        active = "ON" if self.voice.is_active() else "OFF"
        self.ax.set_title(f"Freq: {freq:.1f} HZ | Frames: {self.frames} | Status {active}")
        self.ax.figure.canvas.draw_idle()

    def update_frames(self, delta: int) -> None:
        self.frames = max(1, self.frames+delta)
        new_maxlen = self.frames * self.samples_per_frame
        self.buffer = collections.deque(self.buffer, maxlen=new_maxlen)
        self.ax.set_xlim(0, new_maxlen)


def oscilloscope_main() -> None:
    voice = Voice()
    fig, ax = plt.subplots()
    scope = Oscilloscope(ax, voice, frames = 10, samples_per_frame=2205)
    fig.canvas.draw()
    plt.pause(0.1)


    tables = [SINE, TRIANGLE]
    current_table = 0

    semitone_offset = 0
    fine_offset = 0
    base_freq = 440.0
    key_freq = base_freq
    key_down = False
    def _semitone_offset(offset: int) -> float:
        return 2 ** (offset / 12)

    def update_frequency() -> None:
        nonlocal key_freq
        freq = base_freq * _semitone_offset(semitone_offset) * (1 + fine_offset/1200)
        key_freq = freq
        voice._osc.frequency = key_freq 

    def on_key_press(event: KeyEvent) -> None:
        nonlocal semitone_offset, fine_offset, current_table, tables, key_down, key_freq 
        match event.key:
            case "up":
                semitone_offset = min(12, semitone_offset + 1)
                update_frequency()
            case "down":
                semitone_offset = max(-12, semitone_offset - 1)
                update_frequency()
            case "left":
                scope.update_frames(-1)
            case "right":
                scope.update_frames(1)
            case "z":
                fine_offset = max(-10, fine_offset - 1)
                update_frequency()
            case "x":
                fine_offset = min(10, fine_offset + 1)
                update_frequency()
            case " ":
                if not key_down:
                    key_down = True
                    voice.note_on(key_freq)
            case "r":
                semitone_offset = 0
                fine_offset = 0
                update_frequency()
            case "t":
                current_table = (current_table + 1)%len(tables)
                voice.change_table(tables[current_table])
            case _:
                pass
        

    def generator() -> Generator[None, None, None]:
        while True:
            yield None

    def on_key_release(event: KeyEvent) -> None:
        nonlocal key_down
        if ( event.key == " " or event.key == "space" ) and key_down:
            voice.note_off()
            key_down = False

    _ = fig.canvas.mpl_connect("key_press_event", on_key_press)  # pyright: ignore[reportArgumentType]
    _ = fig.canvas.mpl_connect("key_release_event", on_key_release)  # pyright: ignore[reportArgumentType]
    
    ani = anim.FuncAnimation(fig, scope.update, generator, interval=50, cache_frame_data=False)
    plt.show()

if __name__ == "__main__":
    controls = """
    up/down     - increase/decrease frequency by 1 semitone (Initial freq A3 - 440Hz)
    x/z         - increase/decrease frequency by 1cent
    left/right  - increase/decrease number of generated frames to display. each frame is a 20ms signal chunk.
    space       - triggers note. holding donw note is currently non-functional due to keyboard rettrigering.
    r           - resets frequency to 440Hz
    t           - toggles between available tables.
    q           - closes interface.
    """
    print(controls)
    oscilloscope_main()


