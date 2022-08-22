//
// Created by melodic on 02/06/2020.
//

#include "diffamr_base/diffamr_hw_node.h"
#include <hardware_interface/joint_command_interface.h>
#include <hardware_interface/joint_state_interface.h>

diffamr_hw_node::diffamr_hw_node() {

    pos_sub=nodeHandle.subscribe("motor_pos",10,&diffamr_hw_node::positionCallback,this);
    motor_pub=nodeHandle.advertise<diffamr_msgs::DriverVelocityVal>("driver_cmd_vel",10);

    this->load_params();
    this->initEncoders();

    this->left_wheel.init("left_wheel_joint");
    this->right_wheel.init("right_wheel_joint");

    hardware_interface::JointStateHandle left_state_handle(
        this->left_wheel.joint_name,
        &this->left_wheel.pose,
        &this->left_wheel.velocity,
        &this->left_wheel.effort
    );

    hardware_interface::JointStateHandle right_state_handle(
        this->right_wheel.joint_name,
        &this->right_wheel.pose,
        &this->right_wheel.velocity,
        &this->right_wheel.effort
    );

    joint_state_interface.registerHandle(left_state_handle);
    joint_state_interface.registerHandle(right_state_handle);

    hardware_interface::JointHandle left_handle(
        joint_state_interface.getHandle(this->left_wheel.joint_name), &this->left_wheel.command);

    hardware_interface::JointHandle right_handle(
        joint_state_interface.getHandle(this->right_wheel.joint_name), &this->right_wheel.command);

    position_joint_interface.registerHandle(left_handle);
    position_joint_interface.registerHandle(right_handle);
    velocity_joint_interface.registerHandle(left_handle);
    velocity_joint_interface.registerHandle(right_handle);
    effort_joint_interface.registerHandle(left_handle);
    effort_joint_interface.registerHandle(right_handle);
    //<1>
    registerInterface(&joint_state_interface);
    registerInterface(&effort_joint_interface);
    registerInterface(&velocity_joint_interface);
    registerInterface(&position_joint_interface);
}

void diffamr_hw_node::positionCallback(const diffamr_msgs::DriverPositionSteps &msg)
{
    motor_left_round=msg.mot2_pos_steps;
    motor_right_round=msg.mot1_pos_steps;
    motor_left_vel=msg.mot2_vel_val;
    motor_right_vel=msg.mot1_vel_val;


}

void diffamr_hw_node::load_params() {

    this->node_name = ros::this_node::getName();
    if (this->nodeHandle.hasParam("diffamr_diff_drive_controller/wheel_radius"))
        this->nodeHandle.getParam("diffamr_diff_drive_controller/wheel_radius", this->wheel_radius);
    else
        this->wheel_radius = 0.1;

    if (this->nodeHandle.hasParam("diffamr_diff_drive_controller/use_encoder_velocity"))
        this->nodeHandle.getParam("diffamr_diff_drive_controller/use_encoder_velocity", this->use_encoder_velocity);
    else
        this->use_encoder_velocity = false;

    ROS_INFO_STREAM(this->node_name << "\n\tParameters loaded : "
                                    << "\n\t\t wheel_radius: " << this->wheel_radius
                                    << std::endl);
}

void diffamr_hw_node::initEncoders() { // <1>
    
    boost::shared_ptr<diffamr_msgs::DriverPositionSteps const> pos_msg;
    pos_msg = ros::topic::waitForMessage<diffamr_msgs::DriverPositionSteps>("motor_pos");
    this->left_wheel.encoder = pos_msg->mot1_pos_steps;
    this->right_wheel.encoder = pos_msg->mot2_pos_steps;
    std::cout << "init left encoder: " << this->left_wheel.encoder << std::endl;
    std::cout << "init right encoder: " << this->right_wheel.encoder << std::endl;
}


void diffamr_hw_node::read(ros::Duration &period) { // <2>

    ros::spinOnce();

    this->left_wheel.en_diff = motor_left_round - this->left_wheel.encoder;
    this->right_wheel.en_diff = motor_right_round - this->right_wheel.encoder;

    this->left_wheel.encoder = motor_left_round ;
    this->right_wheel.encoder = motor_right_round;

    this->left_wheel.pose = motor_left_round * 2 * M_PI;
    this->right_wheel.pose = motor_right_round * 2 * M_PI;

    if (period.toSec() > 0) {
        // angluar velocities of wheels (rad/s)
        if (use_encoder_velocity)
        {
            this->left_wheel.velocity = (double(this->left_wheel.en_diff) * 2 * M_PI) / period.toSec();
            this->right_wheel.velocity = (double(this->right_wheel.en_diff) * 2 * M_PI) / period.toSec();
        }else
        {
            this->left_wheel.velocity = (motor_left_vel*(2*M_PI))/60;
            this->right_wheel.velocity = (motor_right_vel*(2*M_PI))/60;
        }
    }

}

void diffamr_hw_node::write(ros::Duration &period) { // <3>

    velMsg.index=0;
    velMsg.mot1_vel_val=0;
    velMsg.mot2_vel_val=0;

    velMsg.mot2_vel_val = (this->left_wheel.command * 60)/(2*M_PI);
    velMsg.mot1_vel_val = (this->right_wheel.command * 60)/(2*M_PI);

    motor_pub.publish(velMsg);
   
}


