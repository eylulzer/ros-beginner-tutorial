cmake_minimum_required(VERSION 2.8.3)
project(diffamr_base)


find_package(catkin REQUIRED COMPONENTS
    controller_manager
    hardware_interface
    roscpp
    diffamr_msgs
    )

catkin_package(
)

include_directories(
    include
    ${catkin_INCLUDE_DIRS}

)

add_library(diffamr_hw_node
    src/diffamr_hw_node.cpp
    include/diffamr_base/diffamr_hw_node.h
    include/diffamr_base/WheelJointState.h
)

add_dependencies(diffamr_hw_node diffamr_msgs_generate_messages_cpp)

add_executable(diffamr_hardware_interface
    src/diffamr_hardware_interface.cpp
)
add_dependencies(diffamr_hardware_interface diffamr_msgs_generate_messages_cpp)

target_link_libraries(
    diffamr_hardware_interface
    diffamr_hw_node
    ${catkin_LIBRARIES}
    )




