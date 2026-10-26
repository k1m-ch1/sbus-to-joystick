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

Then install:

```
pip install -r ./requirements_windows.txt
```


