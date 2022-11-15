#!/usr/bin/env python3

import rospy
from dowaksa_amr_msgs.msg import ButtonPress


def main():
    rospy.init_node('smach_button')
    r = rospy.Rate(10)
    pub = rospy.Publisher("/buttonpressed", ButtonPress, queue_size=10)
    pub2 = rospy.Publisher("/charge", ButtonPress, queue_size=10)
    btn = ButtonPress()

    while not rospy.is_shutdown():
        print("----press-button-----")
        button = int(input())
        if button == 1 or button == 2 or button == 5 or button == 6: 
            btn.buttonPressed = button
            pub.publish(btn)
        else:
            btn.buttonPressed = button
            pub2.publish(btn)
            print("--- charge publish --->", button)

        




if __name__ == '__main__':

    msg = """
    Publishing to Button
    ---------------------------
    Keys:

    1 = Go to 1. goal
    2 = Go to 2. goal
    5 = Emergency
    6 = Deactivate Emergency

    ---------------------------
    """

    print(msg)
    main()
