import sys
import re
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def plot_signal(file_name, sig_name, raw_time_deltas, baudrate, bits_per_char):
    fig, ax = plt.subplots()
    plt.gcf().canvas.manager.set_window_title(f"IR signal plot ('{file_name}')")
    plt.subplots_adjust(bottom=0.25)

    # t as in "time", l as in "level"
    t = []
    l = []
    start_level = 0  # logical start level (should be 0 or 1); level is toggled for every delta t

    fig.suptitle(f"signal '{sig_name}', baudrate: {baudrate}, bits per character: {bits_per_char}")

    bit_width = 1/baudrate*1e6  # bit width, in us, i.e. 1e-6 s
    char_width = bits_per_char*bit_width
    visible_time = 1*char_width

    current_l = start_level
    current_t = 0
    t.append(current_t)
    l.append(current_l)
    for e in raw_time_deltas:
        current_t += e
        t.append(current_t)
        l.append(current_l)
        current_l = 1 - current_l
        t.append(current_t)
        l.append(current_l)

    plt.plot(t, l, "r")
    ax.set_xlim(0, visible_time)
    ax_pos = plt.axes([0.2, 0.1, 0.65, 0.03])
    spos = Slider(ax_pos, 'Pos', 0, max(t) - visible_time, valinit=0., valstep=visible_time)

    def update(val):
        pos = spos.val
        ax.set_xlim(pos, pos + visible_time)
        fig.canvas.draw_idle()

    spos.on_changed(update)

    plt.show()


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: python3 {sys.argv[0]} <IR_file_name> <IR_signal_name>")
    else:
        fname = sys.argv[1]
        req_signal_name = sys.argv[2]
        print(f"Trying to open file '{fname}' and then to plot signal '{req_signal_name}'")
        found = False
        with open(fname) as ir_file:
            txt = ir_file.read()
            # use a regular expression to parse the IR file (note: lines must be in specific order)
            rx = re.compile(r"^name: (.+)(?:\n|\r\n?)type: raw(?:\n|\r\n?)frequency: .+(?:\n|\r\n?)" +
                            r"duty_cycle: .+(?:\n|\r\n?)data: (.+)(?:\n|\r\n?)", re.MULTILINE)
            for match in rx.finditer(txt):
                signal_name, signal_raw = match.groups()
                if signal_name == req_signal_name:
                    print("Found signal:")
                    print(f"  Raw signal name: {signal_name}")
                    print(f"  Raw signal data: {signal_raw}")
                    found = True
                    break

        if found:
            raw = [int(dt) for dt in signal_raw.split()]
            br = 2400  # baud, i.e. 1/s; TODO: make a command line argument
            bpc = 1+8+1+1  # 1 start bit, 8 data bit, 1 parity bit, 1 stop bit; TODO: make a command line argument
            plot_signal(fname, signal_name, raw, br, bpc)
        else:
            print("Unable to find signal in file.")
