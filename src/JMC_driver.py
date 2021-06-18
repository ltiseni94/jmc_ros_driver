#!/usr/bin/python3
# coding: utf-8

import numpy as np
import socket
import rospy

class JMC_driver:

    def __init__(self, IP_config=("192.168.0.10",9999,"192.168.0.100",11111)):
    
        self.micro_IP = IP_config[0]
        self.micro_port = IP_config[1]
        self.personal_IP = IP_config[2]
        self.personal_port = IP_config[3]
        
        # user specified attributes
        
        self.button = np.uint8(0)
        self.send_position = np.float32(0.0)
        
        # echo attributes
        
        self.receive_control_mode = np.uint8(0)
        self.receive_position = np.float32(0.0)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.personal_IP, self.personal_port))
        
        
    def __str__(self):
        return 'smc_driver(' + str(self.micro_IP) + ',' + str(self.micro_port) + ')\n'
        
        
    def __repr__(self):
        print('smc_driver(' + str(self.micro_IP) + ',' + str(self.micro_port) + ')\n')
        
        
    def print_attributes(self):
        print('Desired attributes:\n')
        print('Position:'+ str(self.send_position) + '\n')
        
        print('\n')
        
        print('Current attributes:\n')
        print('Control mode:'+ str(self.receive_control_mode) + '\n')
        print('Position:'+ str(self.receive_position) + '\n')
        
        print('\n')
        
        
    def set_desired_position(self, dp):
        self.send_position = np.single(dp)
        
        
    def set_axis(self, x):
        self.send_axis = np.single(x)
        
        
    def set_buttons(self, button):
        self.button = np.uint8(button)
        
        
    def send_to_driver(self):
        
        control_mode_button_bytes = self.button.tobytes()
        position_bytes = self.send_position.tobytes()
        
        output_bytes = control_mode_button_bytes + position_bytes

        self.sock.sendto(output_bytes, (self.micro_IP, self.micro_port))
        
        
    def receive_from_driver(self):
        
        data, _ = self.sock.recvfrom(5)
        self.receive_control_mode = np.frombuffer(data, dtype=np.uint8, count = 1, offset = 0)
        self.receive_position = np.frombuffer(data, dtype=np.float32, count = 1, offset = 1)
        
        
    def driver_echo(self):
        
        print('Current attributes:\n')
        print('Control mode:'+ str(self.receive_control_mode) + '\n')
        print('Position:'+ str(self.receive_position) + '\n')
        print('\n')

    def logging(self):
        rospy.loginfo('mode: {name}\t angle: {position}'.format(name=self.receive_control_mode, position=self.receive_position))

