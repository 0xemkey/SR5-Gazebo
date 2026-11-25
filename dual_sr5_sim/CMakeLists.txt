cmake_minimum_required(VERSION 3.8)
project(dual_sr5_sim)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    config
    launch
    models
    urdf
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/dual_sr5_gamepad_ik.py
    scripts/udp_joy_bridge.py
    scripts/prepare_dual_sr5.sh
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
