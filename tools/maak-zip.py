"""Maakt downloads/Huize-Briers-huisstijl.zip opnieuw en synchroniseert regels.txt en huisstijl.txt met de .md-bestanden. Draai dit na elke wijziging in logo's, kleuren of regels:
    python3 tools/maak-zip.py
"""
import os, shutil, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Sommige AI-tools (zoals ChatGPT) weigeren text/markdown. Daarom bieden we dezelfde tekst ook als .txt aan (text/plain).
for naam in ("regels", "huisstijl"):
    shutil.copyfile(os.path.join(root, naam + ".md"), os.path.join(root, naam + ".txt"))
out = os.path.join(root, "downloads", "Huize-Briers-huisstijl.zip")
bestanden = []
for map_ in ("logo", os.path.join("logo", "png"), os.path.join("logo", "bistro")):
    for f in sorted(os.listdir(os.path.join(root, map_))):
        p = os.path.join(map_, f)
        if os.path.isfile(os.path.join(root, p)) and f.lower().endswith((".svg", ".png")):
            bestanden.append(p)
bestanden += [os.path.join("downloads", "kleuren.css"), os.path.join("downloads", "kleuren.json"), "huisstijl.md", "regels.md"]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in bestanden:
        z.write(os.path.join(root, p), os.path.join("Huize-Briers-huisstijl", p))
print(len(bestanden), "bestanden in", out)

# Het AI-pakket: script, logo's, lettertypes en de regels als tekst, om aan een AI-project te geven.
pakket = os.path.join(root, "downloads", "Huize-Briers-AI-pakket.zip")
ai = os.path.join(root, "ai-pakket")
with zipfile.ZipFile(pakket, "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, _, files in os.walk(ai):
        for f in sorted(files):
            if f.startswith(".") or f == "__pycache__":
                continue
            p = os.path.join(dirpath, f)
            z.write(p, os.path.join("Huize-Briers-AI-pakket", os.path.relpath(p, ai)))
    for naam in ("regels.txt", "huisstijl.txt"):
        z.write(os.path.join(root, naam), os.path.join("Huize-Briers-AI-pakket", naam))
print("AI-pakket:", pakket)
