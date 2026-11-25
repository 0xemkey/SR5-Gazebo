# System Architecture

## Overview
Dual ROKAE xMate SR5 simulation using ROS 2 Humble and Gazebo Classic.

## Components
- `dual_sr5_sim/launch/dual_sr5_sim.launch.py`: main simulation and teleoperation launch file.
- `dual_sr5_sim/models/dual_sr5_table.sdf`: table model.
- `dual_sr5_sim/urdf/`: left and right SR5 descriptions.
- `dual_sr5_sim/config/sr5_controllers.yaml`: controller configuration.
- `dual_sr5_sim/scripts/udp_joy_bridge.py`: UDP-to-ROS 2 joystick bridge.
- `dual_sr5_sim/scripts/dual_sr5_gamepad_ik.py`: joystick processing and inverse-kinematics teleoperation.
- `tools/windows/gamepad_sender_50hz.py`: Windows F710 publisher.

## Data flow
1. Windows reads Logitech F710 input.
2. The publisher sends JSON over UDP to WSL.
3. The UDP bridge publishes joystick data to ROS 2.
4. The IK node processes commands for the selected arm.
5. ROS 2 controllers execute the resulting commands.

The left and right arms use separate ROS 2 namespaces.
