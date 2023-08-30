from prettytable import PrettyTable
from pythoncaninit import can_init
import can
from udsoncan.connections import PythonIsoTpConnection
from udsoncan.client import Client
import isotp
import config


def check_alive(requestid,responseid):
    flag = False
    can_init()
    filters = config.get_filters()
    isotp_params = config.get_isotp_params()
    bus = can.Bus(can_filters=filters)

    tp_addr = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=requestid, rxid=responseid) # Network layer addressing scheme
    stack = isotp.CanStack(bus=bus, address=tp_addr, params=isotp_params)                        # Network/Transport layer (IsoTP protocol)
    stack.set_sleep_timing(0, 0)                                                                 # Speed First (do not sleep)
    conn = PythonIsoTpConnection(stack)                                                          # interface between Application and Transport layer

    with Client(conn, request_timeout=1) as client:                                              # Application layer (UDS protocol)
        try:
            client.change_session(1)
            flag = True
        except:
            flag =False

    bus.shutdown()
    
    return flag


if '__main__' == __name__:
    requestid = int(input("Please input UDS request id [7xx]: "),16)
    responseid = int(input("Please input UDS response id [7xx]: "),16)
    result = check_alive(requestid,responseid)
    x = PrettyTable()
    x.field_names = ['UDS REQUEST ID','UDS RESPONSE ID','RESULT']
    x.add_row([hex(requestid),hex(responseid),result])
    print(x)
