# simple-hdlc
Simple HDLC Protocol

Used for simple communication with devices. Framing of serial data.

## Usage

Use with instance of In/Output with read and write methods (like pyserial).

```python
s = serial.Serial('/dev/tty0')
h = HDLC(s)
h.sendFrame(b"hello")
print h.readFrame()  # Blocking
```
