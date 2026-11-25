#!/usr/bin/env bash
set -e

export PATH=/usr/bin:/bin:$PATH

source /opt/ros/humble/setup.bash

colcon \
  --log-base ~/ros2_ws/log_dual_repo \
  build \
  --base-paths ~/ros2_ws/src/rokae_ros2 \
               ~/projects/dual-sr5-teleoperation/dual_sr5_sim \
  --packages-up-to dual_sr5_sim \
  --packages-skip rokae_hardware rokae_example \
  --build-base ~/ros2_ws/build_dual_repo \
  --install-base ~/ros2_ws/install_dual_repo \
  --symlink-install

echo
echo "Build tamamlandı."
echo "Launch paketi: $(ros2 pkg prefix dual_sr5_sim)"
