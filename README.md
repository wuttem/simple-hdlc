# simple-hdlc
Simple HDLC Protocol

Used for simple communication with devices. Framing of serial data.

## Usage

Use with instance of In/Output with read and write methods (like pyserial).

Blocking Read:

```python
from simple_hdlc import HDLC
import serial 

s = serial.serial_for_url('loop://', timeout=1)
# or
# s = serial.Serial('/dev/tty0')

h = HDLC(s)
h.sendFrame(b"hello")
print h.readFrame()  # Blocking
```

Reader Thread with callback:

```python
from simple_hdlc import HDLC
import serial

s = serial.serial_for_url('loop://', timeout=1)
h = HDLC(s)
# or
# s = serial.Serial('/dev/tty0')

def frame_callback(data):
    print(data)

h.startReader(onFrame=frame_callback)
h.sendFrame(b"hello")
```