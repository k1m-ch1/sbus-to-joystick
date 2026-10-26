# Flashing to the ESP32

First, we must install the SBUS decoder for the ESP32

```
arduino-cli lib install "Bolder Flight Systems SBUS"
```

Then we can compile and upload the firmware to the ESP32:

```
./upload ./esp32Firmware/ /dev/ttyUSB0
```

Make sure it's working by inspecting the output:

```
tio -b 115200 /dev/ttyUSB0
```

# Linux

create a virtual environment:

```
python3 -m venv .venv
```

Activate it:

```
source ./.venv/bin/activate
```

And then install the required libraries:

```
pip install -r requirements_linux.txt
```

To run it:

```
sudo ./.venv/bin/python ./main.py
```

Now you should see a joystick interface:

```
/dev/input/js0
```

which you can test with jstest

# Windows

We use `vjoy`. So we must install it [here](https://sourceforge.net/projects/vjoystick).

Activate it:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you can't due to permission issues, then that's fine also

If you've activated it:

```
pip install -r requirements_windows.txt
```

Otherwise:

```
.\.venv\Scripts\pip.exe install -r requirements_windows.txt
```

And then you can run it:

```
.\.venv\Scripts\python.exe main_windows.py
```
