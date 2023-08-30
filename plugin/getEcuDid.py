from typing import Any, Optional
from prettytable import PrettyTable
from pythoncaninit import can_init
import can
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
from udsoncan.Response import Response
from udsoncan.Request import Request
from udsoncan import services
import udsoncan.configs
import isotp


isotp_params = {
    'stmin' : 32,                          # Will request the sender to wait 32ms between consecutive frame. 0-127ms or 100-900ns with values from 0xF1-0xF9
    'blocksize' : 8,                       # Request the sender to send 8 consecutives frames before sending a new flow control message
    'wftmax' : 0,                          # Number of wait frame allowed before triggering an error
    'tx_data_length' : 8,                  # Link layer (CAN layer) works with 8 byte payload (CAN 2.0)
    'tx_data_min_length' : None,           # Minimum length of CAN messages. When different from None, messages are padded to meet this length. Works with CAN 2.0 and CAN FD.
    'tx_padding' : 0,                      # Will pad all transmitted CAN messages with byte 0x00.
    'rx_flowcontrol_timeout' : 1000,       # Triggers a timeout if a flow control is awaited for more than 1000 milliseconds
    'rx_consecutive_frame_timeout' : 1000, # Triggers a timeout if a consecutive frame is awaited for more than 1000 milliseconds
    'squash_stmin_requirement' : False,    # When sending, respect the stmin requirement of the receiver. If set to True, go as fast as possible.
    'max_frame_size' : 4095,               # Limit the size of receive frame.
    'can_fd' : True                        # Support CAN FD (Need to change python-can configuration)
}

class BinCodeC(udsoncan.DidCodec):
    def __init__(self, packstr: str | None = None):
        super().__init__(packstr)
    def encode(self, *did_value: Any) -> bytes:
        return did_value[0]
    def decode(self, did_payload: bytes) -> Any:
        return did_payload
    def __len__(self) -> int:
        raise self.ReadAllRemainingData

didconfig={0xF190: BinCodeC}

def read_all_did(requestid,responseid):

    DIDLIST = []

    can_init()
    bus = can.Bus()

    tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=requestid, rxid=responseid) # Network layer addressing scheme
    stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)                        # Network/Transport layer (IsoTP protocol)
    stack.set_sleep_timing(0, 0)                                                                 # Speed First (do not sleep)
    conn = PythonIsoTpConnection(stack)                                                          # interface between Application and Transport layer

    with Client(conn, request_timeout=2) as client:                                              # Application layer (UDS protocol)
        for i in range(0x0000,0xFFFF):
            try:
                req = services.ReadDataByIdentifier.make_request([i],{i: BinCodeC})
                response = client.send_request(req)
                DIDLIST.append([i,response.data[2:]])
            except Exception as e:
                if e.response.code != 0x13:
                    print(hex(i),hex(e.response.code))
                pass
    bus.shutdown()
    print(DIDLIST)
    return DIDLIST
    
def character_pharse(data):
    newdata = ""
    for i in data:
        if i>0x1F and not 0x7A<i<0xA0:
            newdata += bytes([i]).decode('latin')
        else:
            newdata += '*'
    return newdata

if '__main__' == __name__:
    requestid = int(input("Please input UDS request id [7xx]: "),16)
    responseid = int(input("Please input UDS response id [7xx]: "),16)
    # requestid = 0x741
    # responseid  = 0x749
    result = read_all_did(requestid,responseid)
    x = PrettyTable()
    x.field_names = ['DID NO.','HEX DATA','LATIN DATA']
    for i in result:
        x.add_row([hex(i[0]),i[1].hex(),character_pharse(i[1])])
    print(x)
