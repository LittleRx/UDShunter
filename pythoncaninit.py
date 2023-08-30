import configparser
import can

CONFIGPATH = "./etc/can.conf"


## init python can configuration

def can_init():
    config = configparser.ConfigParser()
    config.read(CONFIGPATH)
    for key in config['default'].keys():
        can.rc[key] = config['default'][key]
