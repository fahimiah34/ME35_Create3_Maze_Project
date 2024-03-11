import sys 
import rclpy
from rclpy.node import Node
import random
import requests # you may need to run 'pip install requests' to install this library
import json 
import time
from geometry_msgs.msg import Twist

class RobotMotion():
    def __init__(self):
        print("Motion initialized")

class MotionPublisher(Node):
    def __init__(self):    
        super().__init__('motion_publisher')

        self.cp = RobotMotion()

        print('Creating publisher')
        self.motion_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        '''
        The timer allows the callback to execute every 2 seconds, with a counter iniitialized.
        '''
        print('Creating a callback timer') 
        timer_period = .01
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.previous_rotation = 0
        self.previous_translational = 0

    def timer_callback(self):
        current_time = self.get_clock().now()

        r = requests.get(url = URL, headers = Headers, params = {})
        data = r.json()
        # new_rotation = data['records'][1]['fields']['Value']
        # new_translation = data['records'][2]['fields']['Value']

        msg = Twist()

        linear_x = data['records'][2]['fields']['Value']
        angular_z = data['records'][1]['fields']['Value']

        try: 
            linear_x = float(linear_x)
            angular_z = float(angular_z)
        except: 
            linear_x = 0
            angular_z = 0
            
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        
        self.motion_publisher.publish(msg) 
    def reset(self):
        print('Resetting motion')

        



''' This function makes a get request to the airtable API which will tell us how fast to spin the wheels'''
''' Format: 'https://api.airtable.com/v0/BaseID/tableName '''
URL = 'https://api.airtable.com/v0/applK0NRaebYim73c/Control_Table'


''' Format: {'Authorization':'Bearer Access_Token'}
Headers = {'Authorization':'Bearer patdq1umq6dz00Wjg.1fa65436b75bc5e22d7d04d39029973f64a8cc0c2057984e84e58a1947f50132'}


def main(args = None):
    rclpy.init(args=args)
    motion = MotionPublisher()
    print('Callbacks are called')
    try:
        rclpy.spin(motion)
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')
    finally:
        print("Done")
        motion.reset()
        motion.destroy_node()
        print('shutting down')
        rclpy.shutdown()

if __name__ == '__main__':
    main()
