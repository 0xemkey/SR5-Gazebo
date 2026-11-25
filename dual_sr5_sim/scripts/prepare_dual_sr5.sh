#!/usr/bin/env bash
set -e

source /opt/ros/humble/setup.bash
conda deactivate 2>/dev/null || true

BASE="$HOME/ros2_ws/src/dual_sr5_sim"
CONFIG="$BASE/config/sr5_controllers.yaml"
URDF="$BASE/urdf"
PEDESTAL="$BASE/models/dual_sr5_pedestal.sdf"

echo "======================================"
echo "DUAL SR5 SIMULATION PREPARATION"
echo "======================================"

# 1. Check files
for file in "$CONFIG" "$PEDESTAL" \
  "$URDF/xMateSR5_left.urdf" \
  "$URDF/xMateSR5_right.urdf"; do
    if [[ ! -f "$file" ]]; then
        echo "ERROR: Missing file: $file"
        exit 1
    fi
done

# 2. Validate YAML
python3 - "$CONFIG" <<'PY'
import sys, yaml
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)

required = [
    "/left/controller_manager",
    "/right/controller_manager",
    "/left/arm_controller",
    "/right/arm_controller",
]
for key in required:
    if key not in data:
        raise SystemExit(f"Missing YAML section: {key}")
print("YAML validation: OK")
PY

# 3. Check XML
python3 - "$URDF" <<'PY'
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

base = Path(sys.argv[1])
for side in ("left", "right"):
    path = base / f"xMateSR5_{side}.urdf"
    root = ET.parse(path).getroot()
    plugins = root.findall(".//plugin[@filename='libgazebo_ros2_control.so']")
    if len(plugins) != 1:
        raise SystemExit(f"{side}: expected exactly one Gazebo control plugin")

    namespace = plugins[0].findtext("./ros/namespace")
    if namespace != f"/{side}":
        raise SystemExit(f"{side}: incorrect plugin namespace: {namespace}")

    print(f"{side.upper()} URDF: OK")
PY

echo
echo "Preparation complete."
echo
echo "NEXT:"
echo "1. Start Gazebo in WSL 1."
echo "2. Start left publisher in WSL 6."
echo "3. Start right publisher in WSL 7."
echo "4. Spawn pedestal and both robots in WSL 2."
