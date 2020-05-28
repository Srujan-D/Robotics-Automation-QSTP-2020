#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32

rad = 0.5  #Default radius

def radius_pub():
    rad = Float32(input("Enter Radius"))
    pub = rospy.Publisher('radius', Float32, queue_size=10)
    rospy.init_node('radius_pub', anonymous = True)
    rate = rospy.Rate(50) # 50 Hz

    while not rospy.is_shutdown():
        global rad
        pub.publish(rad)
        rate.sleep

if __name__ == '__main__':
    try:
        radius_pub()
    except rospy.ROSInterruptException:
        pass