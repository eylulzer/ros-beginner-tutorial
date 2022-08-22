cmake_minimum_required(VERSION 3.0.2)
project(diffamr_control)

find_package(catkin REQUIRED COMPONENTS 
  geometry_msgs 
  roscpp 
  sensor_msgs
  diffamr_msgs
)

catkin_package(
    INCLUDE_DIRS include
    LIBRARIES ${PROJECT_NAME}
    CATKIN_DEPENDS geometry_msgs roscpp sensor_msgs
)

include_directories(include ${catkin_INCLUDE_DIRS})

add_library(${PROJECT_NAME} src/diffamr_teleop_twist_joy)
add_dependencies(${PROJECT_NAME}  diffamr_msgs_generate_messages_cpp)
target_link_libraries(${PROJECT_NAME} ${catkin_LIBRARIES})

add_executable(diffamr_teleop_node src/diffamr_teleop_node.cpp)

add_dependencies(diffamr_teleop_node diffamr_msgs_generate_messages_cpp)
target_link_libraries(diffamr_teleop_node ${PROJECT_NAME} ${catkin_LIBRARIES})
set_target_properties(diffamr_teleop_node
  PROPERTIES OUTPUT_NAME diffamr_teleop_node PREFIX "")


