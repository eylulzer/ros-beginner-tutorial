#!/usr/bin/env python

import rospy

#task 1. import the Pose type from the module turtlesim
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
import time
from std_srvs.srv import Empty

x=0
y=0
z=0
yaw=0

def poseCallback(pose_message):

    global x
    global y,z,yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def move(speed,distance, goal):
    
    velocity_message = Twist()
    x0 = x
    y0 = y

    velocity_message.linear.x = speed
    velocity_message.linear.y = speed
    distance_moved = 0.0
    loop_rate = rospy.Rate(1)
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)
    while True:
        rospy.loginfo("Turtlesim moves forwards")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

        distance_moved = distance_moved + abs(0.5 * math.sqrt(((x-x0)**2)+((y-y0)**2)))
        print (distance_moved , " ----- ",x)
        if not (x < goal):
            rospy.loginfo("reached")
            break
        #if not (distance_moved < distance):
        #    rospy.loginfo("reached")
        #    break
    
    
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_publisher.publish(velocity_message)

if __name__ == '__main__':
    try:

        #reset_turtle = rospy.ServiceProxy('reset',Empty)
        #reset_turtle()
        
        rospy.init_node('turtlesim_motion_pose', anonymous=True)        

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)


       #task 2. subscribe to the topic of the pose of the Turtlesim
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic,Pose, poseCallback)
        #?????-----------------------------değişkenler??
        time.sleep(2)
        print ('move: ')
        move (1, 5.0, 10.0)
        time.sleep(2)
        print ('start reset: ')
        rospy.wait_for_service('reset')
        reset_turtle = rospy.ServiceProxy('reset',Empty)
        reset_turtle()
        print ('end reset: ')
       #task 3. spin
        #rospy.spin()

       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")