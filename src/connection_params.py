from collections import namedtuple

IP_Config = namedtuple("IP_Config", ["localIP", "localPort", "remoteIP", "remotePort"])

avatar_IP_Config = IP_Config("192.168.0.10", 9999, "192.168.0.100", 11111)
