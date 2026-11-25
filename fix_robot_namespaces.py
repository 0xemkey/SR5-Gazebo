from pathlib import Path
import re
import shutil

launch_file = Path(
    "dual_sr5_sim/launch/dual_sr5_sim.launch.py"
)

if not launch_file.exists():
    raise FileNotFoundError(f"Launch file not found: {launch_file}")

text = launch_file.read_text()

robots = {
    "left": "/left",
    "right": "/right",
}

for robot, namespace in robots.items():
    topic_line = f'"-topic", "/{robot}/robot_description",'
    namespace_line = f'"-robot_namespace", "{namespace}",'

    count = text.count(topic_line)

    if count != 1:
        raise RuntimeError(
            f"{robot}: Expected exactly one topic line, found {count}"
        )

    # Already configured? Do nothing.
    pattern = re.escape(topic_line) + r"\s*\n\s*" + re.escape(namespace_line)

    if re.search(pattern, text):
        print(f"{robot}: namespace already configured")
        continue

    text = text.replace(
        topic_line,
        topic_line + "\n            " + namespace_line,
        1,
    )

backup = launch_file.with_suffix(".launch.py.bak")
shutil.copy2(launch_file, backup)

launch_file.write_text(text)

print("\nBoth robot namespaces configured:")
print("  left  -> /left")
print("  right -> /right")
print(f"\nBackup: {backup}")
