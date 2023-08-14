# from can.interface import Bus


# sudo modprobe vcan
# Create a vcan network interface with a specific name
# sudo ip link add dev vcan0 type vcan
# sudo ip link set vcan0 up

import time
import can

interface = 'socketcan'
channel = 'vcan0'

def producer(id):
    """:param id: Spam the bus with messages including the data id."""
    bus = can.Bus(channel=channel, interface=interface)
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], is_extended_id=False)
        bus.send(msg)

    time.sleep(1)

producer(10)