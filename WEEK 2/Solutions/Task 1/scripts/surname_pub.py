#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def surname_pub():
    pub = rospy.Publisher('surname', String, queue_size=10)
    rospy.init_node('surname_pub', anonymous = True)
    rate = rospy.Rate(0.1) #10 hz

    while not rospy.is_shutdown():
        sur_name = "Deolasee"
        rospy.loginfo(sur_name)
        pub.publish(sur_name)
        rate.sleep

if __name__ == '__main__':
    try:
        surname_pub()
    except rospy.ROSInterruptException:
        pass
