#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def firstname_pub():
    pub = rospy.Publisher('name', String, queue_size=10)
    rospy.init_node('first_name_pub', anonymous = True)
    rate = rospy.Rate(10) #10 Hz

    while not rospy.is_shutdown():
        fname = "Srujan"
        rospy.loginfo(fname)
        pub.publish(fname)
        rate.sleep

if __name__ == '__main__':
    try:
        firstname_pub()
    except rospy.ROSInterruptException:
        pass
