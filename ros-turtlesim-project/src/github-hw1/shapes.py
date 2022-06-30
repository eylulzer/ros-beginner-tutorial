#!/usr/bin/env python

import math
from time import time
from turtle import clear, color
import rospy
import random
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import Empty



def poseCallback(pose_message):
    global pose_x, pose_y, yaw
    pose_x= pose_message.x
    pose_y= pose_message.y
    yaw = pose_message.theta



def circle(r):
    
    velocity_message = Twist()
    yaw0 = yaw
    loop_rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        velocity_message.linear.x = r
        velocity_message.angular.z = 1
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        print(yaw, yaw0)
        if (yaw-yaw0) <= 0.03 and (yaw-yaw0) >= 0:
            velocity_message.linear.x = 0
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            break

        
def square(k):

    i=0
    for i in range(4):  
        move()
        rotate()


def move():

    velocity_message = Twist()
    x0 = pose_x
    y0 = pose_y
    loop_rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        velocity_message.linear.x = 2
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance = math.sqrt((pose_x-x0)**2+(pose_y-y0)**2)
        print(distance)
        if distance >= k:
            velocity_message.linear.x = 0
            velocity_publisher.publish(velocity_message)
            break

def rotate():

    velocity_message = Twist()
    loop_rate = rospy.Rate(60)
    velocity_message.angular.z = 2
    t0 = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():

        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        loop_rate.sleep()

        if (2*(t1-t0)) >= 1.55:
            velocity_message.angular.z = 0
            velocity_publisher.publish(velocity_message)
            print('son konum : ' ,pose_x,pose_y,yaw)
            break


def change_background():
    rospy.set_param('turtlesim/background_b',random.randint(0,255))
    rospy.set_param('turtlesim/background_g',random.randint(0,255))
    rospy.set_param('turtlesim/background_r',random.randint(0,255))
    clr = rospy.ServiceProxy('clear', Empty)
    clr()          


if __name__ == '__main__':

    while not rospy.is_shutdown():
        try:
            rospy.init_node('cmd_vel_pub', anonymous=True)        

            pose_subscriber = rospy.Subscriber('turtle1/pose', Pose, poseCallback) 
            velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1)

            print ('çizmek istediğiniz şekli giriniz:')
            fig = input()
            if fig == 'circle' or fig == 'çember':
                change_background()
                print ('yarıçapı giriniz:')
                r = float(input())
                circle(r)
            elif fig == 'square' or fig == 'kare':
                change_background()
                print ('kenar uzunluğunu giriniz:')
                k = float(input())
                square(k)
            elif fig == 'k':
                print('son konum : ' ,pose_x,pose_y,yaw)
            elif fig == 'r':
                reset_turtle = rospy.ServiceProxy('reset', Empty)
                reset_turtle()
                clr = rospy.ServiceProxy('clear', Empty)
                clr()
            else:
                print ('geçersiz şekil')


        except rospy.ROSInterruptException:
            rospy.loginfo("node terminated.")