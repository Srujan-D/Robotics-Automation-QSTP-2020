#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Point, PoseStamped
from nav_msgs.msg import Path
from std_msgs.msg import Float32MultiArray
import sys
import numpy as np 
from pid_control.msg import points

rospy.init_node('pub_point', anonymous = True)

class Publish():
    def __init__(self):
        
        self.goals = Path()
        self.goals.header.frame_id = "/turtlebot3_empty_world"
        #self.goals.header.str = rospy.Time.now()
        self.goal_path = PoseStamped()
        self.goal = Point()
        self.n_point = 0
        self.n = points()
        self.rate = rospy.Rate(50) # 50 Hz
        self.pub = rospy.Publisher('path', points, queue_size = 10)
        self.flag = True
        self.j = 0
    def Publish_path(self):
        self.n_point = int(input("Enter number of points in Path "))
        self.n_x = []
        self.n_y = []
        self.n_z = []
        if(self.flag == True):
            for i in range(self.n_point):
                self.goal.x = float(input("Enter x "))
                self.n_x += [self.goal.x]
                self.goal.y = float(input("Enter y "))
                self.n_y += [self.goal.y]
                self.n_z += [float(0)]
                self.n.x = self.n_x
                self.n.y = self.n_y
                self.n.z = self.n_z
                print("...........")
            self.flag = False    
        

        while (not rospy.is_shutdown()):
            
            rospy.loginfo(self.n)
            self.pub.publish(self.n)
            self.flag = False
            self.rate.sleep()

if __name__ == "__main__":
    o = Publish()
    o.Publish_path()
