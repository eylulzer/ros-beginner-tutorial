#!/usr/bin/env python

import sys
import rospy
from ros_essentials_cpp.srv import Elevator
from ros_essentials_cpp.srv import ElevatorRequest
from ros_essentials_cpp.srv import ElevatorResponse

def elevator_client(x):
    rospy.wait_for_service('elevator')
    try:
        elevator = rospy.ServiceProxy('elevator', Elevator)
        resp1 = elevator(x)
        return resp1.req_floor
    except rospy.ServiceException(e):
        print ("Service call failed: %s"%e)

def usage():
    return 

if __name__ == "__main__":
    if len(sys.argv) == 2:
        floor = int(sys.argv[1])
    else:
        print ("%s [floor] "%sys.argv[0])
        sys.exit(1)
    print ("Requesting %s"%(floor))
    s = elevator_client(floor)
    print (s)
