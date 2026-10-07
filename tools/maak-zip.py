"""Maakt downloads/Huize-Briers-huisstijl.zip opnieuw. Draai dit na elke wijziging in logo's, kleuren of regels:
    python3 tools/maak-zip.py
"""
import os, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(root, "downloads", "Huize-Briers-huisstijl.zip")
bestanden = []
for map_ in ("logo", os.path.join("logo", "png")):
    for f in sorted(os.listdir(os.path.join(root, map_))):
        p = os.path.join(map_, f)
        if os.path.isfile(os.path.join(root, p)) and f.lower().endswith((".svg", ".png")):
            bestanden.append(p)
bestanden += [os.path.join("downloads", "kleuren.css"), os.path.join("downloads", "kleuren.json"), "huisstijl.md", "regels.md"]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in bestanden:
        z.write(os.path.join(root, p), os.path.join("Huize-Briers-huisstijl", p))
print(len(bestanden), "bestanden in", out)
