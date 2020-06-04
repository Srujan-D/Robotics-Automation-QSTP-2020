#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Point
import sys
import numpy as np 

rospy.init_node('pub_point', anonymous = True)

class Publish():
    def __init__(self):
        self.goal = Point()
        self.rate = rospy.Rate(50) # 50 Hz
        self.pub = rospy.Publisher('path', Point, queue_size = 10)
        self.goal.x = float(sys.argv[1])
        self.goal.y = float(sys.argv[2])

    def Publish_path(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.goal)
            self.rate.sleep()

if __name__ == "__main__":
    o = Publish()
    o.Publish_path()
