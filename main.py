import can
import time



# sudo modprobe can
# sudo modprobe can-raw
# sudo modprobe peak_usb
# sudo ip link set can0 up type can fd on bitrate 500000 dbitrate 2000000 sample-point 0.875 



class Server:
    def __init__(self,uds_id):
        self.uds_request_id = uds_id
        self.uds_response_id = 0x000
        self.uds_ecu_secret_key = 0x000






















def main():

    ecu01 = Server(0x701)




if __name__ == "__main__":
    main()