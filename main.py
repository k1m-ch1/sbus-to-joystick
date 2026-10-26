#!/usr/bin/env python3

import serial
from evdev import UInput, AbsInfo, ecodes as e

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

NUM_CHANNELS = 16

# SBUS channel values are commonly around 172–1811,
# although the actual range depends on the receiver.
SBUS_RANGE = [
    (600, 1400),
    (600, 1400),
    (200, 1800),
    (600, 1400)
]
SBUS_MIN = []
SBUS_MAX = []
SBUS_MID = []
for min_value, max_value in SBUS_RANGE:
    SBUS_MIN.append(min_value)
    SBUS_MAX.append(max_value)
    SBUS_MID.append((min_value + max_value) // 2)

# Four analog axes.
AXES = [
    e.ABS_X,
    e.ABS_Y,
    e.ABS_RX,
    e.ABS_RY,
]

# Twelve buttons controlled by SBUS channels 5–16.
BUTTONS = [
    e.BTN_SOUTH,
    e.BTN_EAST,
    e.BTN_NORTH,
    e.BTN_WEST,
    e.BTN_TL,
    e.BTN_TR,
    e.BTN_TL2,
    e.BTN_TR2,
    e.BTN_SELECT,
    e.BTN_START,
    e.BTN_MODE,
    e.BTN_THUMBL,
]

AXIS_MIN = -32768
AXIS_MAX = 32767

capabilities = {
    e.EV_ABS: [
        (
            axis,
            AbsInfo(
                value=0,
                min=AXIS_MIN,
                max=AXIS_MAX,
                fuzz=0,
                flat=0,
                resolution=0,
            ),
        )
        for axis in AXES
    ],
    e.EV_KEY: BUTTONS,
}


def sbus_to_axis(value: int, min_value:int, mid_value: int, max_value: int) -> int:
    """Map an SBUS channel value to a signed joystick axis."""

    value = max(min_value, min(max_value, value))

    # Normalize to [-1, 1], with the midpoint at zero.
    normalized = (
        (value - mid_value)
        / ((max_value - min_value) / 2)
    )

    return round(
        max(-1.0, min(1.0, normalized)) * AXIS_MAX
    )


def main():
    with UInput(
        events=capabilities,
        name="ESP32 SBUS Joystick",
        vendor=0x1209,
        product=0x0001,
        version=1,
    ) as joystick:

        print("Virtual joystick created.")
        print("Reading SBUS data from", SERIAL_PORT)

        with serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=1,
        ) as ser:

            while True:
                line = ser.readline().decode(
                    "ascii",
                    errors="ignore",
                ).strip()

                if not line:
                    continue

                try:
                    channels = [
                        int(value)
                        for value in line.split(",")
                    ]
                except ValueError:
                    continue

                if len(channels) != NUM_CHANNELS:
                    continue

                # Channels 1–4 -> joystick axes.
                for index, axis in enumerate(AXES):
                    joystick.write(
                        e.EV_ABS,
                        axis,
                        sbus_to_axis(channels[index], SBUS_MIN[index], SBUS_MID[index], SBUS_MAX[index]),
                    )

                # Channels 5–16 -> buttons.
                #
                # Values above the midpoint are pressed.
                for index, button in enumerate(BUTTONS):
                    channel_value = channels[index + 4]

                    pressed = int(
                        channel_value > SBUS_MID[2]
                    )

                    joystick.write(
                        e.EV_KEY,
                        button,
                        pressed,
                    )

                # Flush all events as one logical update.
                joystick.syn()


if __name__ == "__main__":
    main()
