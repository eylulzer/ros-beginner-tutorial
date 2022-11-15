#!/usr/bin/env python3

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import *
from basic_smach.msg import ButtonPress


landmarks = {
            1: {id: 1,
                'position':{
                    'x': 4.5,
                    'y': 1.5,
                    'z': 0.0
                },
                'orientation':{
                    'w': 0.65,
                    'x': 0.0,
                    'y': 0.0,
                    'z': 0.7
                    }
                },
            2: {id: 2,
                'position':{
                    'x': 2.8,
                    'y': 5.1,
                    'z': 0.0
                },
                'orientation':{
                    'w': 0.4,
                    'x': 0.0,
                    'y': 0.0,
                    'z': -0.9
                    }
                },
            3: {id: 3,
                'position':{
                    'x': -0.06,
                    'y': 5.0,
                    'z': 0.0
                },
                'orientation':{
                    'w': 0.66,
                    'x': 0.0,
                    'y': 0.0,
                    'z': -0.74
                    }
                }
            }


class Idle(smach.State):



    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['drive', 'emergency', 'charge','end'],
                             output_keys=['goal_output'])
        self.state = "Idle"
        rospy.Subscriber("/buttonpressed", ButtonPress, self.ButtonCb)

        rospy.Subscriber("/charge", ButtonPress, self.ChargeCb)

        self.btn = 0
        self.chrg = 100

    def ButtonCb(self, msg):
        self.btn = msg.buttonPressed

    def ChargeCb(self, msg):
        self.chrg = msg.buttonPressed

    def execute(self, userdata):

        rospy.loginfo('Idle State')
        r = rospy.Rate(10)

        while not rospy.is_shutdown():
            if self.btn == 1 or self.btn == 2:
                userdata.goal_output = self.btn
                return 'drive'
            elif self.btn == 5:
                return 'emergency'
            elif self.chrg <= 40:
                return 'charge'
            else:
                r.sleep()


class Drive(smach.State):

    goalReached = "Waiting"


    def __init__(self):
        smach.State.__init__(self,
                             # return etmesi gereken çıktılar
                             outcomes=['success', 'failed', 'charge','emergency'],
                             input_keys=['goal_input'],
                             output_keys=['goal_output'])

        self.btn = 0
        self.chrg = 95

        self.state = "Drive"
        rospy.Subscriber("/buttonpressed", ButtonPress, self.ButtonCb)
        rospy.Subscriber("/charge", ButtonPress, self.ChargeCb)


    def ButtonCb(self, msg):
        self.btn = msg.buttonPressed

    def ChargeCb(self, msg):
        self.chrg = msg.buttonPressed

    def execute(self, userdata):  # input keysler userdata
        rospy.loginfo('go to goal')

        self.goalID = userdata.goal_input
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        Drive.goalReached = "Waiting"
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = landmarks[self.goalID]['position']['x']
        goal.target_pose.pose.position.y = landmarks[self.goalID]['position']['y']
        goal.target_pose.pose.orientation.w = landmarks[self.goalID]['orientation']['w']
        goal.target_pose.pose.orientation.z = landmarks[self.goalID]['orientation']['z']

        client.send_goal(goal, done_cb=Drive.done_cb)
        # client.wait_for_result()

        while not rospy.is_shutdown():

            if self.btn == 5:
                client.cancel_goal()
                return 'emergency'
            # elif self.btn == 1 or self.btn == 2:
            #     userdata.goal_output = self.btn
            #     return 'failed'
            elif self.chrg <= 40:
                return 'charge'
            if Drive.goalReached == 'Reached':
                return 'success'
            elif Drive.goalReached == 'Failed':
                return 'failed'
            # else:
            #     print("----else---")
            #     if Drive.goalReached == 'Reached':
            #         return 'success'
            #     else:
            #         userdata.goal_output = self.btn
            #         return 'failed'

    def done_cb(state, result):
        if state == GoalStatus.SUCCEEDED:
            Drive.goalReached = 'Reached'
        else:
            Drive.goalReached = 'Failed'


class Emergency(smach.State):

    

    def __init__(self):
        smach.State.__init__(self,
                            outcomes=['deactivate'])
        self.state = "Emergency"
        rospy.Subscriber("/buttonpressed",ButtonPress, self.ButtonEm)
        self.btn = 0

    def ButtonEm(self,msg):
        self.btn = msg.buttonPressed

    def execute(self,userdata):
        
        rospy.loginfo('Emergency State')

        while not rospy.is_shutdown():
            if self.btn == 6:
                return 'deactivate'
        

class Charge(smach.State):

    def __init__(self):
        smach.State.__init__(self,
                             outcomes=['end','failed','drive'],
                             )

        self.state = "Charge"
        self.btn = 0
        self.chrg = 35
        rospy.Subscriber('/buttonpressed',ButtonPress, self.ButtonEm)
        rospy.Subscriber('/charge',ButtonPress, self.ChargeCb)


    def ButtonEm(self,msg):
        self.btn = msg.buttonPressed

    def ChargeCb(self, msg):
        self.chrg = msg.buttonPressed

    def execute(self, userdata):
        
        rospy.loginfo('Charging..')
        while not rospy.is_shutdown():
            self.chrg = self.chrg + 5
            rospy.loginfo(self.chrg)
            if self.chrg >= 95:
                return 'end'
            if self.btn == 5:
                return 'failed'
            # elif self.btn == 1 or self.btn == 2:
            #     userdata.goal_output = self.btn
            #     return 'drive'


def main():
    rospy.init_node('example_state_machine')
    rospy.loginfo('State Machine Start')

    sm = smach.StateMachine(outcomes=['End'])

    with sm:
        smach.StateMachine.add('Idle', Idle(),
                               transitions={'drive': 'Drive',
                                            'emergency': 'Emergency',
                                            'charge': 'Charge',
                                            'end': 'End'},
                               remapping={'goal_output': 'goal'})

        smach.StateMachine.add('Drive', Drive(),
                               transitions={'success': 'Idle',
                                            'failed': 'Drive',
                                            'charge': 'Charge',
                                            'emergency': 'Emergency'},
                               remapping={'goal_input': 'goal',
                                          'goal_output': 'goal'})

        smach.StateMachine.add('Emergency', Emergency(),
                                transitions={'deactivate': 'Idle'})

        smach.StateMachine.add('Charge', Charge(),
                               transitions={'end': 'Idle',
                                            'drive': 'Drive',
                                            'failed': 'Emergency'},
                               )


    sm.execute()
    rospy.spin()


if __name__ == '__main__':
    print("----smach-----")
    main()
