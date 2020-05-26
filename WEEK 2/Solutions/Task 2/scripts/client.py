#!/usr/bin/env python
import rospy
import sys
from polar_cart_serv_client.srv import convert, convertRequest, convertResponse

rospy.init_node("client", anonymous=True)

class Client():
    def __init__(self):
        self.client = rospy.ServiceProxy("opt_coordinates", convert)
        self.response = convertResponse()
        self.request = convertRequest()
        self.request.first_coordinate = float(sys.argv[1])
        self.request.second_coordinate = float(sys.argv[2])
        self.request.to_polar = int(sys.argv[3])

    def get_response(self):
        print(sys.argv[0])
        self.response = self.client(self.request)
        print(self.response)

if __name__=="__main__":
    rospy.wait_for_service("opt_coordinates")
    o=Client()
    o.get_response()
