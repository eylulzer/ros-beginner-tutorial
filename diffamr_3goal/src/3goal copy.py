#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal


class Goals():

    def __init__(self):
        self.sub = rospy.Subscriber("chatter",String,self.callback)

    def movebase_client():

        # Create an action client called "move_base" with action definition file "MoveBaseAction"
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

        # Waits until the action server has started up and started listening for goals.
        client.wait_for_server()
        rospy.loginfo("waiting 5 sec")
        rospy.sleep(5.)
        rospy.loginfo("done!")
        # Creates a new goal with the MoveBaseGoal constructor
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goals =[[-1.769, 1.599, 0.547], [-1.874, -1.383 , 0.685], [-0.036, -6.723 , 0.637], [-1.049, -13.307, 0.738]]
        for i in range(2):
            # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
            goal.target_pose.pose.position.x = goals[i][0]
            goal.target_pose.pose.position.y = goals[i][1]
            # No rotation of the mobile base frame w.r.t. map frame
            goal.target_pose.pose.orientation.w = goals[i][2]

            # Sends the goal to the action server.
            client.send_goal(goal)
            # Waits for the server to finish performing the action.
            wait = client.wait_for_result()
            # If the result doesn't arrive, assume the Server is not available
            #if not wait:
            #    rospy.logerr("Action server not available!")
            #    rospy.signal_shutdown("Action server not available!")
            #else:
            #   Result of executing the action
            rospy.sleep(5.)
        return client.get_result()

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
        # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")