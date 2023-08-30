from prettytable import PrettyTable
from pythoncaninit import can_init
import can
import time

TIMEOUT = 0.03
SERVERID = 0x00

filters = [
    {"can_id": 0x700, "can_mask": 0xF00, "extended": False},
]

def parseData(msg):
    global SERVERID
    if SERVERID == 0:
        if (msg.arbitration_id & 0x700) == 0x700 :
            if msg.data[1] == 0x50 and msg.data[2] == 0x01:
                SERVERID = msg.arbitration_id

def detect_canid(bus,uds_request_id):
    global SERVERID
    SERVERID = 0
    uds_data = [0x02,0x10,0x01,0x00,0x00,0x00,0x00,0x00]
    bus.send(can.Message(arbitration_id=uds_request_id,data=uds_data))
    notifier = can.Notifier(bus,[parseData],TIMEOUT)
    time.sleep(TIMEOUT)
    notifier.stop()
    return SERVERID

def uds_detecter():
    UDSLIST = []
    can_init()
    bus = can.Bus(can_filters=filters)
    for requestid in [i for i in range(0x700,0x7FF) if i!= 0x7DF]:
        serviceid = detect_canid(bus,requestid)
        if serviceid != 0:
            UDSLIST.append([requestid,serviceid])
    bus.shutdown()
    return UDSLIST

if '__main__' == __name__:
    udslist = uds_detecter()
    x = PrettyTable()
    x.field_names = ['No.','UDS REQUEST ID','UDS RESPONSE ID']
    for i in range(len(udslist)):
        x.add_row([hex(i),hex(udslist[i][0]),hex(udslist[i][1])])
    x.add_row(['Functional','0x7DF','EVERY ECU'])
    print(x)
