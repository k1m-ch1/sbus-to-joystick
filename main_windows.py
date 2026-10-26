import serial
import pyvjoy

SERIAL_PORT = "COM3"  # Change to your ESP32's COM port
BAUD_RATE = 115200

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



NUM_CHANNELS = 16

# vJoy axis constants
AXES = [
    pyvjoy.HID_USAGE_X,
    pyvjoy.HID_USAGE_Y,
    pyvjoy.HID_USAGE_Z,
    pyvjoy.HID_USAGE_RX,
]

VJOY_MIN = 0x1
VJOY_MAX = 0x8000


def sbus_to_vjoy(value, min_value, mid_value, max_value):
    value = max(min_value, min(max_value, value))

    normalized = (
        (value - min_value) / (max_value - min_value)
    )

    return round(
        VJOY_MIN + normalized * (VJOY_MAX - VJOY_MIN)
    )


def main():
    joystick = pyvjoy.VJoyDevice(1)

    with serial.Serial(
        SERIAL_PORT,
        BAUD_RATE,
        timeout=1,
    ) as ser:
        print(f"Reading ESP32 from {SERIAL_PORT}")

        while True:
            line = ser.readline().decode(
                "ascii", errors="ignore"
            ).strip()

            if not line:
                continue

            try:
                channels = [
                    int(v) for v in line.split(",")
                ]
            except ValueError:
                continue

            if len(channels) != NUM_CHANNELS:
                continue

            # First four channels -> analog axes.
            for index, axis in enumerate(AXES):
                joystick.set_axis(
                    axis,
                    sbus_to_vjoy(channels[index], SBUS_MIN[index], SBUS_MID[index], SBUS_MAX[index]),
                )

            # Channels 5–16 -> buttons 1–12.
            for index in range(12):
                pressed = (
                    channels[index + 4] > SBUS_MID[2]
                )

                joystick.set_button(
                    index + 1,
                    int(pressed),
                )


if __name__ == "__main__":
    main()
