#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from turtle_circle.srv import rad_vel, rad_velRequest, rad_velResponse

rospy.init_node("ang_vel_server",anonymous=True)

class Compute_Ang_Vel():
    def __init__(self): 
        self.serv=rospy.Service("compute_ang_vel", rad_vel, self.compute)
        self.response = rad_velResponse()
        self.radius = 0.0
        self.linear_velocity = 0.5

    
    def compute(self, request):
        self.radius = request.radius
        self.angular_velocity = self.linear_velocity/self.radius
        self.response = self.angular_velocity
        return self.response

if __name__=="__main__":
    o = Compute_Ang_Vel()
    rospy.spin()