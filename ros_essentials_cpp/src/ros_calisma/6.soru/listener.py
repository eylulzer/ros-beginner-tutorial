#!/usr/bin/env python
import rospy, tf2_ros, geometry_msgs.msg
if __name__ == '__main__':
    rospy.init_node('listener')
    listener = tf2_ros.TransformListener()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('base_link','base_laser', \
                                                    rospy.Time(0))
    # This will give you the coordinate of the child in the parent frame
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException):
            pass
    rate.sleep()