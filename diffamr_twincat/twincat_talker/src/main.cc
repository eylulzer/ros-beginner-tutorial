#include "AdsLib.h"
#include "AdsNotification.h"
#include "AdsVariable.h"
#include "ros/ros.h"
#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <geometry_msgs/Twist.h>
#include <diffamr_msgs/DriverPositionSteps.h>
#include <diffamr_msgs/DriverVelocityVal.h>




float rpmgx;
float rpmgw;
float rad = 0.17;        // wheel radius
float multip = 9.549;   // 60/π --- fixed multiplier used to convert from mt/s to rpm 


void teleopCallback(const geometry_msgs::Twist& msg)
{
    ROS_INFO("Msg linear x: [%f]", msg.linear.x);
    ROS_INFO("Msg angular w: [%f]", msg.angular.z);
    rpmgx = ((multip * msg.linear.x) / rad);
    rpmgw = ((multip * msg.angular.z) / rad);
}


int main(int argc, char *argv[]) {
  // ROS node init
  ros::init(argc, argv, "tctalker");
  ros::NodeHandle n;
  ROS_INFO_STREAM("running good");

  diffamr_msgs::DriverPositionSteps msgPos;
  diffamr_msgs::DriverVelocityVal msgVel;


  ros::Subscriber sub = n.subscribe("/cmd_vel", 1000, teleopCallback);
  ros::Publisher position_pub = n.advertise<diffamr_msgs::DriverPositionSteps>(std::string("motor_pos"),10);
  ros::Publisher velocity_pub = n.advertise<diffamr_msgs::DriverVelocityVal>(std::string("motor_vel"),10);

  static const AmsNetId remoteNetId{192, 168, 2, 99, 1, 1};
  static const char remoteIpV4[] = "192.168.2.99";

  AdsDevice route{remoteIpV4, remoteNetId, AMSPORT_R0_PLC_TC3};

  AdsVariable<int16_t> variable_to_write_motor_set_mod{route, "MAIN.motorSetMode"};
  AdsVariable<bool> variable_to_write_motor_enable{route, "MAIN.writeMode"};
  AdsVariable<bool> variable_to_write_rpm_enable{route, "MAIN.motorRPMWrite"};  
  AdsVariable<float> variable_to_write_motor_left_rpm{route, "MAIN.motorLeftRPM"};  
  AdsVariable<float> variable_to_write_motor_right_rpm{route, "MAIN.motorRightRPM"};

  
  AdsVariable<float> variable_to_read_left_motor_pos{route, "MAIN.motorLeftPos"};
  AdsVariable<float> variable_to_read_right_motor_pos{route, "MAIN.motorRightPos"};
  AdsVariable<int16_t> variable_to_read_left_motor_vel{route, "MAIN.motorCurrVelLeft"};
  AdsVariable<int16_t> variable_to_read_right_motor_vel{route, "MAIN.motorCurrVelRight"};

  ros::Rate loop_rate(1);

  variable_to_write_motor_set_mod = 8;

  variable_to_write_motor_enable = true;
  ros::Duration(0.1).sleep();
  variable_to_write_motor_enable = false;



  int16_t rpm1;
  int16_t rpm2;
 while (ros::ok())
 {

  float lp = (static_cast<float>(variable_to_read_left_motor_pos));
  float rp = (static_cast<float>(variable_to_read_right_motor_pos)); 
  int16_t lv = int16_t(variable_to_read_left_motor_vel);
  int16_t rv = int16_t(variable_to_read_right_motor_vel); 


  msgPos.index=0;
  msgPos.mot1_pos_steps=lp;
  msgPos.mot2_pos_steps=rp;
  msgPos.mot1_vel_val=lv;
  msgPos.mot2_vel_val=rv;
        
  position_pub.publish(msgPos);

  msgVel.index=0;
  msgVel.mot1_vel_val=lv;
  msgVel.mot2_vel_val=rv;

  velocity_pub.publish(msgVel);


  std::cout << "Left Position: " << lp <<'\n';
  std::cout << "Right Position: " << rp << '\n';
  std::cout << "Left Velocity: " << lv <<'\n';
  std::cout << "Right Velocity: " << rv << '\n';

  if (rpmgw == 0){


    variable_to_write_motor_left_rpm = rpmgx;
    variable_to_write_motor_right_rpm = rpmgx;

  }

  else if (rpmgw >= 0)
  {
    variable_to_write_motor_left_rpm = rpmgx;
    variable_to_write_motor_right_rpm = 0;
  }
  
  else if (rpmgw <= 0)
  {
    variable_to_write_motor_left_rpm = 0;
    variable_to_write_motor_right_rpm = rpmgx;
  }



  variable_to_write_rpm_enable = true;
  ros::Duration(0.1).sleep();
  variable_to_write_rpm_enable = false;

  loop_rate.sleep();
  ros::spinOnce();
 }



  
  return 0;
}
