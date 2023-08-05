Python Solight DY05 library for Raspberry Pi
============================================

This library allows you to control [Solight DY05](https://www.alzashop.com/solight-dy05-2-drawers-1-driver-d3921909.htm) sockets from Raspberry Pi.

How to use it
-------------

Connect cheap [433 MHz transmitter](https://www.robotshop.com/en/seeedstudio-433mhz-low-cost-transmitter-receiver-pair.html) to any GPIO pin (e.g. 17)

```bash
sudo apt-get install pigpio
sudo pip3 install solight-dy05
sudo pigpiod
```

```python
import time
import pigpio
from dy05 import DY05

pi = pigpio.pi()
dy05 = DY05(pi, 17)
address = 42
socket = 1

while True:
	dy05.send(address, socket, 1)
	time.sleep(1)
	dy05.send(address, socket, 0)
	time.sleep(1)
```

After running this script, you should see the socket turning on and off every second.

License
-------

MITNFA
