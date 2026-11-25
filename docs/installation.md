# Installation and Build

## Environment
- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11
- WSL2
- Logitech F710

The upstream ROKAE ROS 2 packages are expected at `~/ros2_ws/src/rokae_ros2`.

## Build
```bash
source /opt/ros/humble/setup.bash
cd ~/projects/dual-sr5-teleoperation

colcon --log-base ~/ros2_ws/log_dual_repo build \
  --base-paths ~/ros2_ws/src/rokae_ros2 \
               ~/projects/dual-sr5-teleoperation/dual_sr5_sim \
  --packages-up-to dual_sr5_sim \
  --packages-skip rokae_hardware rokae_example \
  --build-base ~/ros2_ws/build_dual_repo \
  --install-base ~/ros2_ws/install_dual_repo \
  --symlink-install
```

## Launch
```bash
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install_dual_repo/setup.bash
source ~/gz_control_fix_ws/install/setup.bash
ros2 launch dual_sr5_sim dual_sr5_sim.launch.py
```

## Windows publisher
Install its dependency with `py -m pip install inputs`.
Run `tools/windows/gamepad_sender_50hz.py` on Windows. Confirm its `UDP_IP` matches the current WSL IP. It sends to UDP port 9090 at 50 Hz.
