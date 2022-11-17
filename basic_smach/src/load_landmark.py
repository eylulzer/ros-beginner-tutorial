#!/usr/bin/env python3

import yaml


def loadLandmark():
    
    with open('/home/merve/catkin_ws/src/ros-beginner-tutorial/basic_smach/config/mir_landmarks.yaml') as stream:
        try:
            lm_dict = yaml.safe_load(stream)
            result = 1
            if lm_dict is None:
                lm_dict = {}
                result = 0
        except:
            lm_dict = {}
            result = -1
    
    return lm_dict, result
        

