cmake_minimum_required(VERSION 2.8.3)

add_compile_options(-std=c++11)
project(twincat_talker)

find_package(catkin REQUIRED roscpp diffamr_msgs)

catkin_package(
    CATKIN_DEPENDS roscpp sensor_msgs
)

add_subdirectory(dep/ADS)

include_directories(dep/ADS/AdsLib dep/ADS/AdsLibOOI ${catkin_INCLUDE_DIRS})

add_executable(twincat_talker src/main.cc)
add_executable(twincat_listenner src/listenner.cc)
add_executable(deneme src/deneme.cc)


target_link_libraries(twincat_listenner
    libadscxx
    ${catkin_LIBRARIES}
)
target_link_libraries(twincat_talker
    libadscxx
    ${catkin_LIBRARIES}
)
target_link_libraries(deneme
    libadscxx
    ${catkin_LIBRARIES}
)

install(TARGETS twincat_talker
   ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
   RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)