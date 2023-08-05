Python Solight DY01 library for Raspberry Pi
============================================

This library allows you to control [Solight DY01](https://www.nay.sk/solid-dy01-dialkovo-ovladane-zasuvky-set-3-1) sockets from Raspberry Pi.

How to use it
-------------

Connect a cheap [433 MHz transmitter](https://www.robotshop.com/en/seeedstudio-433mhz-low-cost-transmitter-receiver-pair.html) to any GPIO pin (e.g. 17)

```
sudo apt-get install pigpio
sudo pip3 install solight-dy01
sudo pigpiod
```

```python
import time
import pigpio
from dy01 import DY01

pi = pigpio.pi()
dy01 = DY01(pi, 17)
address = 1007 # Default address of socket A

while True:
	dy01.send(address, 1)
	time.sleep(1)
	dy01.send(address, 0)
	time.sleep(1)
```

After running this script, you should see the socket turning on and off every second.

License
-------

MIT
