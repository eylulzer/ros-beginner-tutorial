#!/usr/bin/env python
# license removed for brevity
import rospy
from turtlesim.msg import Pose



def pose_callBack(pose_msg):
    print ("--------")
    print (pose_msg.x)


if __name__ == "__main__":

    rospy.init_node('get_odometry', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, pose_callBack)

    rospy.spin()
