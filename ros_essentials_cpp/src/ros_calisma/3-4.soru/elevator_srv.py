#!/usr/bin/env python

from ros_essentials_cpp.srv import Elevator
from ros_essentials_cpp.srv import ElevatorRequest
from ros_essentials_cpp.srv import ElevatorResponse

import rospy


def elevatorIsWorking(req):
    if req.floor > 5 or req.floor < 0:
        response = "Geçersiz input"
    else:
        response = "kaldırıldı-indirildi"
    return ElevatorResponse(response)

def elevatorServer():
    rospy.init_node('elevator_server')
    rospy.Service('elevator', Elevator, elevatorIsWorking)
    print ("Elevator is ready.")
    rospy.spin()
    
if __name__ == "__main__":
    elevatorServer()
