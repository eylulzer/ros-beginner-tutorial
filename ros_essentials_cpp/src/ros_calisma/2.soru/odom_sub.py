#!/usr/bin/env python
# license removed for brevity
import rospy
from turtlesim.msg import Pose



def odom_callBack(odom_msg):
    print ("--------")
    print (odom_msg.x)



if __name__ == "__main__":

    rospy.init_node('get_odometry', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, odom_callBack)

    rospy.spin()
