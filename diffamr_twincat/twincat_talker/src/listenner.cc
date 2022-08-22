#include "AdsLib.h"
#include "AdsNotification.h"
#include "AdsVariable.h"
#include "ros/ros.h"
#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <array>
#include <iomanip>
#include <vector>

int main(int argc, char *argv[]) {
  // ROS node init
  ros::init(argc, argv, "tctalker");
  ros::NodeHandle n;
  ROS_INFO_STREAM("running good");

  static const AmsNetId remoteNetId{192, 168, 0, 2, 1, 1};
  static const char remoteIpV4[] = "192.168.0.2";

  AdsDevice route{remoteIpV4, remoteNetId, AMSPORT_R0_PLC_TC3};
   
   while(true) {
    AdsVariable<uint16_t> readVar {route, "MAIN.hallInput[1]"};
    AdsVariable<int16_t> readVar2 {route, "MAIN.hallInput[2]"};
    
   uint32_t abc = (static_cast<uint32_t>(readVar) << 16) + static_cast<uint32_t>(readVar2);

    std::cout << "READVAR " << abc << '\n';

    std::cout << __FUNCTION__ << "():\n";
   /* for (size_t i = 0; i < 1; ++i) {
        std::cout << "ADS read " << (uint16_t)readVar << '\n';
         std::cout << "ADS read " << (int16_t)readVar2 << '\n';
    }*/

    ros::Duration(1).sleep();
   }


 /* AdsVariable<int16_t> variable_to_write_motor_set_mod{route, "MAIN.motorSetMod"};
  AdsVariable<bool> variable_to_write_motor_enable{route, "MAIN.motorEnable"};
  AdsVariable<bool> variable_to_write_rpm_enable{route, "MAIN.motorRPMWrite"};  
  AdsVariable<int16_t> variable_to_write_motor_left_rpm{route, "MAIN.motorLeftRPM"};  
  AdsVariable<int16_t> variable_to_write_motor_right_rpm{route, "MAIN.motorRightRPM"};  

  ros::Rate loop_rate(1);

  variable_to_write_motor_set_mod = 8;

  variable_to_write_motor_enable = true;
  ros::Duration(0.1).sleep();
  variable_to_write_motor_enable = false;

  int16_t rpm;
 while (ros::ok())
 {

  ROS_INFO_STREAM("Motor rpm degeri giriniz: ");
  scanf("%d", &rpm);
  variable_to_write_motor_left_rpm = rpm;
  variable_to_write_motor_right_rpm = rpm;

  variable_to_write_rpm_enable = true;
  ros::Duration(0.1).sleep();
  variable_to_write_rpm_enable = false;

  loop_rate.sleep();
  ros::spinOnce();
 }


*/
  
  return 0;
}
