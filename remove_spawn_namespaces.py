from pathlib import Path
import re
import shutil

launch = Path("dual_sr5_sim/launch/dual_sr5_sim.launch.py")

if not launch.exists():
    raise SystemExit(f"HATA: Dosya bulunamadı: {launch}")

content = launch.read_text()

patterns = [
    r'^[ \t]*"-robot_namespace",\s*"/left",\s*\n',
    r'^[ \t]*"-robot_namespace",\s*"/right",\s*\n',
]

for pattern in patterns:
    matches = re.findall(pattern, content, flags=re.MULTILINE)
    if len(matches) != 1:
        raise SystemExit(
            f"HATA: Beklenen satır tam bir kez bulunmalı. "
            f"Bulunan: {len(matches)}. Dosya değiştirilmedi."
        )

backup = launch.with_suffix(launch.suffix + ".namespace.bak")
shutil.copy2(launch, backup)

updated = content
for pattern in patterns:
    updated = re.sub(pattern, "", updated, count=1, flags=re.MULTILINE)

launch.write_text(updated)

print("İki robot_namespace argümanı kaldırıldı.")
print(f"Yedek: {backup}")
print("\nKontrol:")
for line_no, line in enumerate(updated.splitlines(), 1):
    if "-robot_namespace" in line:
        print(f"UYARI: {line_no}: {line}")

print("İşlem tamamlandı.")
