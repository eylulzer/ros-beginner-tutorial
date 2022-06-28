#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import time



def move(x, y, z):
    
    velocity_message = Twist()
    velocity_message.linear.x = x
    velocity_message.linear.y = y
    velocity_message.angular.z = z
    loop_rate = rospy.Rate(5)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)

    i=0
    while not rospy.is_shutdown():
        
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        i=i+1
        if i == 20:
            break


if __name__ == '__main__':
    try:
        rospy.init_node('cmd_vel_pub', anonymous=True)        

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size = 10)

        time.sleep(2)
        print ('move: ')
        move (1.0, 1.0, 1.0)
        #rospy.spin()

       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")