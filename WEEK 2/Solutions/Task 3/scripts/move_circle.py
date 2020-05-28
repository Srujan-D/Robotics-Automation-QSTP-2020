#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from turtle_circle.srv import rad_vel, rad_velRequest, rad_velResponse

rospy.init_node('move_circle.py', anonymous = True)

class Turtle():
    def __init__(self):
        self.radius = 0.0
        self.sub = rospy.Subscriber('radius', Float32, self.compute_angvel)
        self.rate = rospy.Rate(50) # 50 Hz
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
        self.vel_msg = Twist()                  # Default value of all vel_msg component velocities is 0 due to constructor.
        
    
    def compute_angvel(self, request):          # callback function
        self.radius = request.data              # Get the radius from user
        if(self.radius != 0.0):                 # Once as non zero radius is entered by the user, the turtlebot will start to move.
            self.vel_msg.linear.x = 0.5
        self.client = rospy.ServiceProxy("compute_ang_vel", rad_vel)
        self.response = self.client(self.radius)
        self.vel_msg.angular.z = self.response.angular_vel
        rospy.spin()

    def publish(self):
        while not rospy.is_shutdown():
            if (self.radius != 0.0):            # Once the user enters the radius, the turtlebot3 velocity will be printed on screen.
                print(self.vel_msg)
            self.pub.publish(self.vel_msg)
            self.rate.sleep

if __name__ == "__main__":
    rospy.wait_for_service("compute_ang_vel")
    o = Turtle()
    o.publish()