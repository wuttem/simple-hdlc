# simple-hdlc
Simple HDLC Protocol

Used for simple communication with devices. Framing of serial data.

## Usage

Use with instance of In/Output with read and write methods (like pyserial).

Blocking Read:

```python
s = serial.Serial('/dev/tty0')
h = HDLC(s)
h.sendFrame(b"hello")
print h.readFrame()  # Blocking
```

Reader Thread with callback:

```python
s = serial.Serial('/dev/tty0')
h = HDLC(s)

def frame_callback(data):
    print(data)

h.startReader(onFrame=frame_callback, onError=error_callback)
h.sendFrame(b"hello")
```