import serial
import pyvjoy

SERIAL_PORT = "COM3"  # Change to your ESP32's COM port
BAUD_RATE = 115200

SBUS_MIN = 172
SBUS_MAX = 1811
SBUS_MID = (SBUS_MIN + SBUS_MAX) // 2

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


def sbus_to_vjoy(value):
    value = max(SBUS_MIN, min(SBUS_MAX, value))

    normalized = (
        (value - SBUS_MIN) / (SBUS_MAX - SBUS_MIN)
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
                    sbus_to_vjoy(channels[index]),
                )

            # Channels 5–16 -> buttons 1–12.
            for index in range(12):
                pressed = (
                    channels[index + 4] > SBUS_MID
                )

                joystick.set_button(
                    index + 1,
                    int(pressed),
                )


if __name__ == "__main__":
    main()
