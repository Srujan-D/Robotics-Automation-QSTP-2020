#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from turtle_circle.srv import rad_vel, rad_velRequest, rad_velResponse

import math
flag = False
rospy.init_node('move_infinty.py', anonymous = True)

class Turtle():
    def __init__(self):
        self.radius = 0.0
        self.sub = rospy.Subscriber('radius', Float32, self.compute_angvel)
        self.rate = rospy.Rate(50) # 50 Hz
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        self.vel_msg = Twist()                      # Default value of all vel_msg component velocities is 0 due to constructor.
        self.time = 2*(math.pi)                     # time period of oscillation = 2*PI/angular velocity. We will divide self.time by the angular velocity after we git it through the server.

    def compute_angvel(self, request):              # callback function
        self.radius = request.data
        self.client = rospy.ServiceProxy("compute_ang_vel", rad_vel)
        self.response = self.client(self.radius)
        self.vel_msg.angular.z = self.response.angular_vel
        self.time = self.time/self.vel_msg.angular.z
        rospy.spin()

    def publish(self):
        while not rospy.is_shutdown():
            global change_time
            global flag
            if (flag):
                self.vel_msg.angular.z = abs(self.vel_msg.angular.z)     # 1st loop
                if (self.radius != 0.0):            
                    print("In Loop 1 of the path---------------------------------")
                    self.vel_msg.linear.x = 0.5     # If a non zero radius is entered by the user, the turtlebot will start to move.
                    print(self.vel_msg)             # If the user has entered a nonzero radius, the turtlebot3 velocity will be printed on screen.
                self.pub.publish(self.vel_msg)
            else:
                self.vel_msg.angular.z = -abs(self.vel_msg.angular.z)    # 2nd loop
                if (self.radius != 0.0):            
                    print("In Loop 2 of the path...................")
                    self.vel_msg.linear.x = 0.5     # If a non zero radius is entered by the user, the turtlebot will start to move.
                    print(self.vel_msg)             # If the user has entered a nonzero radius, the turtlebot3 velocity will be printed on screen.
                self.pub.publish(self.vel_msg)
            if (change_time < rospy.Time.now()) :
                flag = not flag
                change_time = rospy.Time.now() + rospy.Duration(self.time)
            self.rate.sleep

if __name__ == "__main__":
    rospy.wait_for_service("compute_ang_vel")
    o = Turtle()
    change_time = rospy.Time.now() 
    o.publish()
