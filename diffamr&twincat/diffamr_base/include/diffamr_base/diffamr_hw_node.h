//
// Created by melodic on 02/06/2020.
//

#ifndef ROS_WORKSPACE_DIFFAMR_HW_NODE_H
#define ROS_WORKSPACE_DIFFAMR_HW_NODE_H

#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/joint_state_interface.h>
#include <hardware_interface/robot_hw.h>
#include "WheelJointState.h"
#include "diffamr_msgs/DriverVelocityVal.h"
#include "diffamr_msgs/DriverPositionSteps.h"
#include <ros/ros.h>
#include <iostream>

class diffamr_hw_node : public hardware_interface::RobotHW {
public:
    diffamr_hw_node();

    void positionCallback(const diffamr_msgs::DriverPositionSteps &msg);

    virtual ~diffamr_hw_node() = default;

    void load_params();

    void initEncoders();

    void read(ros::Duration &period);

    void write(ros::Duration &period);

private:
    std::string node_name;
    hardware_interface::JointStateInterface joint_state_interface;
    hardware_interface::VelocityJointInterface velocity_joint_interface;
    hardware_interface::PositionJointInterface position_joint_interface;
    hardware_interface::EffortJointInterface effort_joint_interface;

    WheelJointState left_wheel;
    WheelJointState right_wheel;

    diffamr_msgs::DriverVelocityVal velMsg;

    ros::NodeHandle nodeHandle;

    ros::Subscriber pos_sub;
    ros::Publisher motor_pub;

    double wheel_radius;
    double motor_left_round;
    double motor_right_round;
    double motor_left_vel;
    double motor_right_vel;
    
    bool use_encoder_velocity;

};


#endif //ROS_WORKSPACE_diffamr_HW_NODE_H
