#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    client.wait_for_server()
    rospy.loginfo("waiting 5 sec")
    rospy.sleep(5.)
    rospy.loginfo("done!")

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goals =[[-1.769, 1.599, 0.547], [-1.874, -1.383 , 0.685], [-0.036, -6.723 , 0.637], [-1.049, -13.307, 0.738]]
    for i in range(2):
 
        goal.target_pose.pose.position.x = goals[i][0]
        goal.target_pose.pose.position.y = goals[i][1]
        goal.target_pose.pose.orientation.w = goals[i][2]

        client.send_goal(goal)
        wait = client.wait_for_result()
        rospy.sleep(5.)
    return client.get_result() 

if __name__ == '__main__':
    try:

        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
