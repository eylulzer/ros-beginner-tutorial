#!/usr/bin/env python3

import rospy
from dowaksa_amr_msgs.msg import ButtonPress
from geometry_msgs.msg import PoseWithCovarianceStamped
import load_landmark as ll
import time


curr_pose = PoseWithCovarianceStamped()

def poseCb(msg):
    global curr_pose
    curr_pose = msg

#robot gönderilen id istasyonunda ise true döner
def checkPose(goalId):

    global curr_pose

    # d = rospy.Duration(3, 0)
    # rospy.sleep(d)
    rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped, poseCb)
    
    #thresholdlar
    pos_th = 0.3
    ori_th = 0.1

    lm_dict, result = ll.loadLandmark()

    abs_x = abs(curr_pose.pose.pose.position.x - lm_dict[goalId]['position']['x'])
    abs_y = abs(curr_pose.pose.pose.position.y - lm_dict[goalId]['position']['y'])

    abs_w = abs(curr_pose.pose.pose.orientation.w - lm_dict[goalId]['orientation']['w'])
    abs_z = abs(curr_pose.pose.pose.orientation.z - lm_dict[goalId]['orientation']['z'])


    if abs_x <= pos_th and abs_y <= pos_th and abs_w <= ori_th and abs_z <= ori_th:
        return True
    
    else:
        return False


