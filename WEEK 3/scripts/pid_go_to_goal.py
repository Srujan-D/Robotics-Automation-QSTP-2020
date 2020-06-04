#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Point, Quaternion, PoseStamped
import sys
from math import pow, atan2, sqrt
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import time
 
class TurtleBot:
 
    def __init__(self, current_time=None):
        rospy.init_node('pid_go_to_goal', anonymous = True)
        self.x = 0.0
        self.y = 0.0
        self.flag = False             # flag and 'a' values will be used for switching between rotation and translation      
        self.a = 1
        self.theta = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.goal = Point()
        self.new_x = self.goal.x - self.x       # this will be an input to actuator response
        self.new_y = self.goal.y - self.y       # this will be an input to actuator response
                                                 
        self.sub = rospy.Subscriber('path', Point, self.get_path)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.get_odom)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
        self.rate = rospy.Rate(50) # 50 Hz
    
        self.Kp = 1.0                           # Default Proportionality Constant                            
        self.Ki = 0.0                           # Default Integral Constant
        self.Kd = 0.0                           # Default Derivative Constant
        self.feedback_value = 0.0               # This will help us in controlling the actuator response  
        self.SetPoint = atan2(self.goal.y, self.goal.x)  # We will compare our feedback_value to the SetPoint value
        self.current_time = current_time if current_time is not None else time.time()  # We will use time difference of short intervals to calculate Integral and Derivative Terms
        self.last_time = self.current_time      # After each iteration we will update the last_time and current time

        self.PTerm = 0.0                        # Default Proportionality Term
        self.ITerm = 0.0                        # Default Integral Term
        self.DTerm = 0.0                        # Default Derivative Term
        self.last_error = 0.0                   # After each iteration we will update the last_error.       

        # Windup Guard - In case the integral term accumulates a significant error during the rise (windup), thus overshooting.
        self.windup_guard = 1000.0             


    def get_path(self, request):
        self.goal = request
        if(self.flag == False):                 # For rotating the turtlebot
            self.SetPoint = atan2(self.goal.y, self.goal.x)
        else:                                   # For translating the turtlebot
            self.SetPoint = sqrt(pow((self.goal.x), 2) + pow((self.goal.y), 2))
            
    def get_odom(self, request):
        self.turtle = request.pose.pose.orientation
        self.x = request.pose.pose.position.x   # Current x coordinate of turtlebot
        self.y = request.pose.pose.position.y   # Current y coordinate of turtlebot
        (self.roll, self.pitch, self.theta) = euler_from_quaternion([self.turtle.x, self.turtle.y, self.turtle.z, self.turtle.w])   # We will only use the yaw value, or the angle (theta) with z axis.
        
    def dist(self, new_y, new_x):               # Calculates distance
        return sqrt(pow((new_x), 2) + pow((new_y), 2))

    def turn_angle(self, new_y, new_x):     # Calculates the angle by which the turtlebot has to turn
        return (atan2(new_y, new_x))

    def calculate(self, new_y, new_x, Kp, Ki, Kd, feedback_value, current_time = None): # Calculates Angular Velocity
        self.error = (self.SetPoint - feedback_value)
        
        current_time = current_time if current_time is not None else time.time()
        self.delta_time = (current_time - self.last_time)
        self.delta_error = self.error - self.last_error
        self.PTerm = self.error
        self.ITerm += self.error * self.delta_time
            
        if (self.ITerm < -self.windup_guard):
            self.ITerm = -self.windup_guard
        elif (self.ITerm > self.windup_guard):
            self.ITerm = self.windup_guard

        self.DTerm = 0.0
        if self.delta_time > 0:
            self.DTerm = self.delta_error / self.delta_time

        # Update the last time and last error for next iteration
        self.last_time = self.current_time
        self.last_error = self.error

        self.output = (Kp * self.PTerm) + (Ki * self.ITerm) + (Kd * self.DTerm)  # Output is the updated angular or linear velocity
        return self.output

    
    
    def move2goal(self, current_time=None):     # Function that commonds the turtlebot
        
        vel_msg = Twist()
 
        while not rospy.is_shutdown(): 
    
            self.new_x = self.goal.x - self.x
            self.new_y = self.goal.y - self.y
            if((self.flag == False) and (round(abs(atan2(self.new_y, self.new_x)-(self.theta)), 3) != 0)): # Precision upto 3 decimal places
                print("Rotating")
                
                self.feedback_value = self.theta
                self.Kp = 0.3
                self.Kd = 0.0000001 
                self.Ki = 0.000001 
                vel_msg.linear.x = 0
                vel_msg.angular.z = self.calculate(self.new_y, self.new_x, self.Kp, self.Ki, self.Kd, self.feedback_value)
            
            else :
                if(self.flag == False ):
                    vel_msg.angular.z = 0.0
                    vel_msg.linear.x = 0.0
                    if(self.a >= 0):            # This condition will help us in stopping the turtlebot for a moment after the required rotation of turtlebot is achived
                        rospy.sleep(1)
                        self.a = self.a-1
                        
                self.flag = True
                vel_msg.angular.z = 0.0
            self.pub.publish(vel_msg)
            
            if ((self.flag == True) and (self.dist(self.new_y, self.new_x) > 0.005)):   # Precision is 0.005
                print("Translating")
                
                self.feedback_value = self.dist(self.y, self.x)
                self.Kp = 0.005
                self.Kd = 0.00001 
                self.Ki = 0.0001
                vel_msg.angular.z = 0.0
                vel_msg.linear.x = self.calculate(self.new_y, self.new_x, self.Kp, self.Ki, self.Kd, self.feedback_value)
                        
            else:
                if(self.flag == True):
                    vel_msg.angular.z = 0.0
                
                self.flag = False
                vel_msg.linear.x = 0
            self.pub.publish(vel_msg)
            self.rate.sleep()
        rospy.spin()

 
if __name__ == '__main__':
    try:
        o = TurtleBot()
        o.move2goal()
    except rospy.ROSInterruptException:
        pass
