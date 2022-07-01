#!/usr/bin/env python
from typing import List
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist



def Lasersc(laser_msg):

    print(" Array uzunluğu: --- ",len(laser_msg.ranges))
    print(" 0 derece uzaklığı: ---",laser_msg.ranges[0])

    vel_msg = Twist()


    vel_msg.linear.x = 0.1

    if laser_msg.ranges[0] <= 1:
        vel_msg.linear.x = 0.0
    
    pub.publish(vel_msg)
        
    
    

# def stopRobot():

#     vel_msg = Twist()
#     loop_rate = rospy.Rate(10)
    

#     While not rospy.is_shutdown()

#         vel_msg.linear.x = 0.5
#         pub.publish(vel_msg)
#         loop_rate.sleep()

#     vel_msg.linear.x = 0
#     pub.publish(vel_msg)


if __name__ == '__main__':

    try:
        rospy.init_node('scan_node',anonymous=True)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        sub = rospy.Subscriber('/scan', LaserScan, Lasersc)
        #stopRobot()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated")
