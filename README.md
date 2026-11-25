# Dual ROKAE xMate SR5 Teleoperation

ROS 2 and Gazebo Classic simulation for dual ROKAE xMate SR5 robotic arms controlled using a Logitech F710 gamepad.

## Features
- Dual SR5 simulation in Gazebo Classic
- Separate ROS 2 control namespaces for left and right arms
- Windows-to-WSL UDP gamepad communication
- Cartesian teleoperation using inverse kinematics
- Independent deadman controls

## Environment
- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11
- WSL2
- Logitech F710

## Dependencies
ROKAE ROS 2 packages are expected at `~/ros2_ws/src/rokae_ros2`.

## Build
```bash
source /opt/ros/humble/setup.bash
cd ~/projects/dual-sr5-teleoperation
colcon --log-base ~/ros2_ws/log_dual_repo build --base-paths ~/ros2_ws/src/rokae_ros2 ~/projects/dual-sr5-teleoperation/dual_sr5_sim --packages-up-to dual_sr5_sim --packages-skip rokae_hardware rokae_example --build-base ~/ros2_ws/build_dual_repo --install-base ~/ros2_ws/install_dual_repo --symlink-install
```

## Launch
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install_dual_repo/setup.bash
source ~/gz_control_fix_ws/install/setup.bash
ros2 launch dual_sr5_sim dual_sr5_sim.launch.py
```

## Windows gamepad publisher
File: `tools/windows/gamepad_sender_50hz.py`
Install dependency: `py -m pip install inputs`
Run from repository root: `py tools\windows\gamepad_sender_50hz.py`
The publisher sends UDP packets to port 9090 at 50 Hz. Update `UDP_IP` if the WSL IP changes.

## Gamepad mapping
| Input | Field |
|---|---|
| Left stick X/Y | axes[0], axes[1] |
| Right stick X/Y | axes[2], axes[3] |
| Triggers | axes[4], axes[5] |
| D-pad X/Y | axes[6], axes[7] |
| A/B/X/Y | buttons[0..3] |
| LB | buttons[4] |
| RB | buttons[5] |
| Select | buttons[6] |
| Start | buttons[7] |

LB controls the left-arm deadman; RB controls the right-arm deadman.

## Safety
- Test in simulation before physical hardware.
- Start with small joystick movements.
- Verify arm directions before increasing speed.
- Keep the robot workspace clear.

## License
Apache License 2.0. See `LICENSE`.

## Further documentation

- [Installation and build](docs/installation.md)
- [System architecture](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Gamepad mapping](teleoperation/docs/gamepad_mapping.md)
