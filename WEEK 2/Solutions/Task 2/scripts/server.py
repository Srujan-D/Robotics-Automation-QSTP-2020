#!/usr/bin/env python
import rospy
import numpy as np
from polar_cart_serv_client.srv import convert, convertRequest, convertResponse

rospy.init_node("server",anonymous=True)

class Service():
    def __init__(self): 
        self.serv=rospy.Service("opt_coordinates", convert, self.conv)
        self.response = convertResponse()
        self.first_coordinate = 0.0
        self.second_coordinate = 0.0
        self.to_polar = 0

    
    def conv(self, request):
        self.first_coordinate = request.first_coordinate
        self.second_coordinate = request.second_coordinate
        self.to_polar = request.to_polar

        if (self.to_polar == 1):
            self.response.conv_first_coordinate, self.response.conv_second_coordinate = cart2pol( float(self.first_coordinate), float(self.second_coordinate))
            return self.response
        else :
            self.response.conv_first_coordinate, self.response.conv_second_coordinate = pol2cart( float(self.first_coordinate), float(self.second_coordinate))
            return self.response


def pol2cart( r, theta):         #function for converting polar to cartesian coordinates.
	x = r*np.cos(theta)
	y = r*np.sin(theta)
	return (x,y)

def cart2pol( x, y):             #function for converting cartesian to polar coordinates.
	r = np.sqrt( x**2 + y**2 )
	theta = np.arctan2(y, x)
	return (r,theta)
   
if __name__=="__main__":
    print("Ready to convert coordinates. Enter x y 1 to convert cartesian coordinates (x, y) to polar coordinates (r, theta). Otherwise enter r theta any_number to convert polar coordinates to cartesian coordinates")
    o = Service()
    rospy.spin()
