#!/usr/bin/env python
import rospy
from std_msgs.msg import String

name0 = "a"
name1 = "b"

def callback0(msg):
    #rospy.loginfo("%s", msg)
    global name0 
    name0 = str(msg.data)
    rospy.spin()

    
def callback1(msg):
    #rospy.loginfo("%s", msg)
    global name1 
    name1 = str(msg.data)
    rospy.spin()

    
def full_name():
    rospy.init_node('fullname_sub_pub', anonymous = True)
    rospy.Subscriber("name", String, callback0)
    rospy.Subscriber("surname", String, callback1)
    pub = rospy.Publisher('fullname', String, queue_size=10)
    rate = rospy.Rate(10) #10 Hz
    #rospy.spin()

    while not rospy.is_shutdown():
        fullname = name0 + " " + name1
        rospy.loginfo(fullname)
        pub.publish(fullname)
        rate.sleep

if __name__ == '__main__':
    try:
        full_name()
    except rospy.ROSInterruptException:
        pass
