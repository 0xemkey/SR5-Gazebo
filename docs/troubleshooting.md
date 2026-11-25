# Troubleshooting

## ROS 2 commands unavailable
Run `source /opt/ros/humble/setup.bash`.

## Package not found
Build the workspace and source `~/ros2_ws/install_dual_repo/setup.bash`. Confirm the upstream ROKAE packages exist at `~/ros2_ws/src/rokae_ros2`.

## No UDP input
- Confirm the Windows publisher is running.
- Confirm `UDP_IP` is the current WSL IP.
- Confirm UDP port 9090 is reachable and not blocked by firewall rules.
- The main launch file starts the bridge; do not start a duplicate bridge.

## Gamepad dependency error
On Windows run `py -m pip install inputs`.

## Controllers do not load
Inspect Gazebo and ROS 2 control logs. Verify the expected `gazebo_ros2_control` plugin and workspace overlay are available.

## Robot does not move
Check UDP reception, joystick topics, IK node status, deadman button state, and controller activation. Inspect the live system with `ros2 topic list` and `ros2 control list_controllers`.
