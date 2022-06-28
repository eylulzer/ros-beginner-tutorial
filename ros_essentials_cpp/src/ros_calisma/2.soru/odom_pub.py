#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

global t
t = Twist ()
t.linear.x = 5.0
t.angular.z = 4.0


def poseCallback(pose_message):

    global p
    p = Pose ()
    p = pose_message

def twCallback(tw_message):

    t = tw_message


def odom_pub():
    
    odom_pub = rospy.Publisher('odometry', Odometry, queue_size=10)
    rospy.init_node('odompub', anonymous=True)
    rate = rospy.Rate(0.5) 
    i = 0
    while not rospy.is_shutdown():
        odom_msg = Odometry()
        odom_msg.header.frame_id = "---Frame id : " + str(i)
        odom_msg.pose.pose = p
        #odom_msg.twist.twist = t
        rospy.loginfo(odom_msg)
        odom_pub.publish(odom_msg)
        rate.sleep()
        i=i+1

if __name__ == '__main__':
    try:
        rospy.Subscriber('/turtle1/pose',Pose, poseCallback)
        rospy.Subscriber('/turtle1/cmd_vel',Twist, twCallback)
        odom_pub()
    except rospy.ROSInterruptException:
        pass
