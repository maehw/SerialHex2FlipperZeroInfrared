import sys
import json

# comments have been left in the code to support understanding what's going on;
# could be migrated to log levels


def convert(name, message, frequency, duty_cycle, baudrate, wait_reply=True):
    timings = []

    # evaluate input data; this can be improved for sure
    assert (isinstance(message, list))

    # always start with an idle line (logic 1)
    # the start bit will always generate an edge
    level = None
    duration = 1

    for msg_chunk_idx in range(len(message)):
        bts = bytearray.fromhex(message[msg_chunk_idx])
        for byte_cnt in range(len(bts)):
            # print(f"0x{bytes[byte_cnt]:02X}: (start)0b", end="")

            # start bit is always logic 0
            if not level:
                # print("s", end="")
                duration += 1
            else:
                # print("↓", end="")
                if byte_cnt > 0:  # non-existent bit before very first start bit shall not be appended
                    timings.append(duration)
                duration = 1
            # print("0", end="")
            level = False

            # print(f" (LSB first)0b", end="")
            parity_cnt = 0
            # from LSBit to MSBit
            for bitpos in range(0, 8):
                if bts[byte_cnt] & (1 << bitpos):
                    if level:
                        # print("S", end="")
                        duration += 1
                    else:
                        # print("↑", end="")
                        timings.append(duration)
                        duration = 1
                    # print("1", end="")
                    level = True
                    parity_cnt += 1
                else:
                    if not level:
                        # print("s", end="")
                        duration += 1
                    else:
                        # print("↓", end="")
                        timings.append(duration)
                        duration = 1
                    # print("0", end="")
                    level = False

            # odd parity bit
            parity_bit = (parity_cnt + 1) % 2
            # print(f" (odd parity bit)0b", end="")
            if parity_bit:
                if level:
                    # print("S", end="")
                    duration += 1
                else:
                    # print("↑", end="")
                    timings.append(duration)
                    duration = 1
                # print("1", end="")
                level = True
                parity_cnt += 1
            else:
                if not level:
                    # print("s", end="")
                    duration += 1
                else:
                    # print("↓", end="")
                    timings.append(duration)
                    duration = 1
                # print("0", end="")
                level = False

            # print(f" (stop bit)0b", end="")
            # stop bit is always logic 1
            # print("1", end="")
            if level:
                # print("S", end="")
                duration += 1
            else:
                # print("↑", end="")
                timings.append(duration)
                duration = 1
            level = True
            parity_cnt += 1

            # print()
            # print(f"\n  timings: {timings}")

            if byte_cnt == len(bts) - 1:
                # print("  --last byte in line--")

                # add some more stop bits/idle time,

                # always assume a short pause is about 2 bytes (1+8+1+1=11 raw bits per byte) long
                duration += 11 * 2

                if wait_reply:
                    # assume length of reply is the same as length of message
                    duration += 11 * (len(bts) + 2)

                timings.append(duration)
                level = None
                duration = 1

        # if msg_chunk_idx == len(message)-1:
        # print("---last line")
        # else:
        # print("---next line---")
        # print(f"\n     timings: {timings}")
        # print()

    # absolute timings in microseconds
    abs_timings = [round(item * 1 / baudrate * 1e6) for item in timings]

    # print("----------")

    out = f"""#
name: {name}
type: raw
frequency: {frequency}
duty_cycle: {duty_cycle}
data: {" ".join(str(time) for time in abs_timings)}"""

    return out


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} input.json")
    else:
        filename = sys.argv[1]
        with open(filename) as json_file:
            data = json.load(json_file)
            # print(data)
            settings = data["settings"]

            print("Filetype: IR signals file")
            print("Version: 1")
            for signal in data["signals"]:
                # print(signal)
                print(convert(signal["name"], signal["msg"], settings["frequency"], settings["duty_cycle"],
                              settings["baudrate"]))
