#!/usr/bin/env python3
"""
Huize Briers: maakt een afgewerkt beeld voor Instagram of Facebook.

Eén echte foto, beeldvullend, met het echte logo, de kop in Bodoni Moda italic 700 en de
praktische regel in Instrument Sans. Marges, lettertypes, kleuren en de plaats van het logo staan vast.

Voorbeeld:
  python3 maak-post.py foto.jpg --kop "De worstenbroodjes zijn terug" \
      --regel "Vanaf donderdag 8 oktober in Bilzen en Munsterbilzen" \
      --plaats "Bilzen · Munsterbilzen" --label "Terug in de winkel"

Voor de bistro: voeg --merk bistro toe. Voor een story: --formaat story.
Alleen de foto en de tekst veranderen. Het product op de foto wordt nooit aangepast.
"""
import argparse
import os
import re
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageStat

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "lettertypes")
LOGOS = os.path.join(HERE, "logo")

FORMATEN = {"feed": (1080, 1350), "story": (1080, 1920), "vierkant": (1080, 1080)}
SAFE = {"story": (250, 340)}  # boven en onder vrij van tekst en logo (interface van Instagram)
INK = (28, 25, 23)
AMBER = (232, 145, 46)
WIT = (255, 255, 255)
MARGE = 72

VERBODEN = ["ambachtelijk", "authentiek", "de allerbeste ingrediënten", "met liefde gemaakt", "dat smaakt naar meer",
            "staat garant voor", "ontdek", "geniet", "heerlijk", "overheerlijk", "een begrip", "heb jij ze al geproefd",
            "heb je ze al geproefd", "valt in de smaak bij iedereen", "100%"]


def lettertype(naam, grootte, gewicht, optisch=None):
    """Laadt een variabel lettertype en zet het gewicht."""
    pad = os.path.join(FONTS, naam)
    f = ImageFont.truetype(pad, int(grootte))
    try:
        if naam.startswith("Bodoni"):
            f.set_variation_by_axes([gewicht, optisch or 11])  # lage optische grootte: de dunne lijntjes blijven zichtbaar
        else:
            f.set_variation_by_axes([100, gewicht])
    except Exception:
        pass
    return f


def bodoni(grootte):
    return lettertype("BodoniModa-Italic.ttf", grootte, 700)


def sans(grootte, gewicht=400):
    return lettertype("InstrumentSans.ttf", grootte, gewicht)


def controleer(teksten):
    """Waarschuwt als de tekst de regels breekt. Stopt niet: de medewerker beslist."""
    kop = teksten["kop"]
    alles = " ".join(v for k, v in teksten.items() if v and k != "label")
    waarschuwingen = []
    if len(kop.split()) > 6:
        waarschuwingen.append(f"De kop heeft {len(kop.split())} woorden. Hoogstens 6.")
    laag = alles.lower()
    gevonden = [w for w in VERBODEN if w in laag]
    if gevonden:
        waarschuwingen.append("Verboden woord: " + ", ".join(gevonden))
    if re.search(r"[–—]| - ", alles):
        waarschuwingen.append("Geen gedachtestreepjes: gebruik een punt of een komma.")
    if re.search(r"\b[A-ZÀ-Ý]{3,}\b", alles):
        waarschuwingen.append("Geen woorden volledig in hoofdletters.")
    if alles.count("!") > 1:
        waarschuwingen.append("Hoogstens één uitroepteken.")
    for w in waarschuwingen:
        print("LET OP:", w, file=sys.stderr)
    return waarschuwingen


def verbeter(img):
    """Alleen technische correcties: belichting, contrast en een beetje scherpte. Geen kleur of inhoud."""
    notities = []
    luma = ImageStat.Stat(img.convert("L")).mean[0]
    if luma < 105:
        gamma = max(0.55, min(1.0, (luma / 118.0) ** 0.6))
        lut = [int(255 * ((i / 255.0) ** gamma)) for i in range(256)]
        img = img.point(lut * 3)
        notities.append(f"belichting omhoog (gemiddelde helderheid {luma:.0f} naar ongeveer 118)")
    elif luma > 175:
        gamma = min(1.5, (luma / 150.0) ** 0.6)
        lut = [int(255 * ((i / 255.0) ** gamma)) for i in range(256)]
        img = img.point(lut * 3)
        notities.append(f"belichting omlaag (gemiddelde helderheid {luma:.0f})")
    img = ImageOps.autocontrast(img, cutoff=0.4)
    notities.append("contrast iets opgetrokken")
    img = img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=3))
    notities.append("licht scherper gemaakt")
    print("Verbeterd:", ", ".join(notities), file=sys.stderr)
    return img


def vul(img, breed, hoog, focus):
    """Foto beeldvullend, uitgesneden rond het focuspunt (0 tot 1). Nooit vervormen."""
    s = max(breed / img.width, hoog / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = round((img.width - breed) * focus[0])
    y = round((img.height - hoog) * focus[1])
    return img.crop((x, y, x + breed, y + hoog))


def verloop(breed, hoog, tekst_boven):
    """Donker verloop in ink achter de tekst, plus een lichte sluier over alles."""
    laag = Image.new("RGBA", (breed, hoog), INK + (0,))
    sluier = Image.new("RGBA", (breed, hoog), INK + (46,))
    laag = Image.alpha_composite(laag, sluier)
    grad = Image.linear_gradient("L")  # 256 hoog: zwart boven, wit onder
    if tekst_boven:
        grad = ImageOps.flip(grad)
    grad = grad.resize((breed, round(hoog * 0.62)))
    masker = Image.new("L", (breed, hoog), 0)
    masker.paste(grad.point(lambda v: int(v * 0.80)), (0, 0 if tekst_boven else hoog - grad.height))
    donker = Image.new("RGBA", (breed, hoog), INK + (255,))
    donker.putalpha(masker)
    return Image.alpha_composite(laag, donker)


def breek(tekst, font, max_breed, tekenaar):
    regels, regel = [], ""
    for w in tekst.split():
        proef = f"{regel} {w}".strip()
        if tekenaar.textlength(proef, font=font) > max_breed and regel:
            regels.append(regel)
            regel = w
        else:
            regel = proef
    if regel:
        regels.append(regel)
    return regels


def spatieer(tekenaar, xy, tekst, font, vul, spatie):
    x, y = xy
    for ch in tekst:
        tekenaar.text((x, y), ch, font=font, fill=vul)
        x += tekenaar.textlength(ch, font=font) + spatie
    return x


def spatie_breedte(tekenaar, tekst, font, spatie):
    return sum(tekenaar.textlength(ch, font=font) + spatie for ch in tekst) - spatie


def plak_logo(basis, pad, breedte, xy):
    logo = Image.open(pad).convert("RGBA")
    hoogte = round(logo.height * breedte / logo.width)
    logo = logo.resize((breedte, hoogte), Image.LANCZOS)
    basis.alpha_composite(logo, xy)
    return hoogte


def maak(a):
    breed, hoog = FORMATEN[a.formaat]
    boven_vrij, onder_vrij = SAFE.get(a.formaat, (0, 0))
    tekst_boven = a.tekst == "boven"

    foto = ImageOps.exif_transpose(Image.open(a.foto)).convert("RGB")
    if a.verbeter:
        foto = verbeter(foto)
    foto = vul(foto, breed, hoog, (a.focus_x, a.focus_y))
    beeld = foto.convert("RGBA")
    if not a.zonder_verloop:
        beeld = Image.alpha_composite(beeld, verloop(breed, hoog, tekst_boven))
    d = ImageDraw.Draw(beeld)

    # logo: wit, in de hoek tegenover de tekst
    if a.merk == "bistro":
        logo_pad, logo_b = os.path.join(LOGOS, "Bistro-Briers-logo-wit.png"), 280
    else:
        logo_pad, logo_b = os.path.join(LOGOS, "Huize-Briers-logo-gestapeld-wit.png"), 250
    probe = Image.open(logo_pad)
    logo_h = round(probe.height * logo_b / probe.width)
    logo_y = (hoog - MARGE - onder_vrij - logo_h) if tekst_boven else (MARGE + boven_vrij)
    plak_logo(beeld, logo_pad, logo_b, (MARGE, logo_y))

    # label (optioneel): één amber vlak, rechtsboven (of rechtsonder bij tekst boven)
    if a.label:
        lf = sans(28, 600)
        tekst = a.label.upper()
        tb = spatie_breedte(d, tekst, lf, 3)
        pw, ph = round(tb + 70), 78
        px = breed - MARGE - pw
        py = (hoog - MARGE - onder_vrij - ph) if tekst_boven else (MARGE + boven_vrij)
        d.rounded_rectangle((px, py, px + pw, py + ph), radius=ph // 2, fill=AMBER)
        spatieer(d, (px + 35, py + (ph - 28) // 2 - 3), tekst, lf, INK, 3)

    # tekstblok
    max_b = breed - 2 * MARGE
    grootte = 112
    while grootte >= 60:
        kf = bodoni(grootte)
        kop_regels = breek(a.kop, kf, max_b, d)
        if len(kop_regels) <= 3:
            break
        grootte -= 4
    kop_lh = round(grootte * 1.04)
    rf = sans(40, 400)
    regel_regels = breek(a.regel, rf, max_b - 120, d) if a.regel else []
    regel_lh = round(40 * 1.32)
    pf = sans(26, 500)
    hoogte_blok = len(kop_regels) * kop_lh
    if regel_regels:
        hoogte_blok += 44 + len(regel_regels) * regel_lh
    if a.plaats:
        hoogte_blok += 46 + 26
    y = (MARGE + boven_vrij) if tekst_boven else (hoog - MARGE - onder_vrij - hoogte_blok)

    for r in kop_regels:
        d.text((MARGE, y), r, font=kf, fill=WIT)
        y += kop_lh
    if regel_regels:
        y += 44
        for r in regel_regels:
            d.text((MARGE, y), r, font=rf, fill=(238, 235, 231))
            y += regel_lh
    if a.plaats:
        y += 46
        d.rectangle((MARGE, y + 12, MARGE + 82, y + 14), fill=AMBER)
        spatieer(d, (MARGE + 82 + 40, y), a.plaats.upper(), pf, (214, 210, 204), 4)

    uit = a.uit or f"post-{a.merk}-{a.formaat}.png"
    beeld.convert("RGB").save(uit, "PNG" if uit.lower().endswith(".png") else "JPEG", quality=94)
    print("Klaar:", os.path.abspath(uit), f"({breed} x {hoog})")


def main():
    p = argparse.ArgumentParser(description="Maakt een afgewerkt beeld voor Huize Briers of Bistro Briers.")
    p.add_argument("foto", help="de echte foto (jpg of png)")
    p.add_argument("--kop", required=True, help="hoogstens 6 woorden")
    p.add_argument("--regel", default="", help="praktische regel: wanneer en waar")
    p.add_argument("--plaats", default="", help="kleine regel onderaan, bijvoorbeeld 'Bilzen · Munsterbilzen'")
    p.add_argument("--label", default="", help="optioneel kort label in een amber vlak, bijvoorbeeld 'Terug in de winkel'")
    p.add_argument("--merk", choices=["huize", "bistro"], default="huize", help="logo: Huize Briers of Bistro Briers")
    p.add_argument("--formaat", choices=list(FORMATEN), default="feed", help="feed 1080x1350, story 1080x1920, vierkant 1080x1080")
    p.add_argument("--tekst", choices=["onder", "boven"], default="onder", help="waar de tekst staat; kies de rustige kant van de foto")
    p.add_argument("--focus-x", type=float, default=0.5, help="0 tot 1: welk deel van de foto blijft staan bij uitsnijden")
    p.add_argument("--focus-y", type=float, default=0.5)
    p.add_argument("--verbeter", action="store_true", help="alleen belichting, contrast en scherpte corrigeren")
    p.add_argument("--zonder-verloop", action="store_true", help="geen donker verloop achter de tekst")
    p.add_argument("--uit", help="bestandsnaam van het resultaat (png of jpg)")
    a = p.parse_args()
    controleer({"kop": a.kop, "regel": a.regel, "plaats": a.plaats, "label": a.label})
    maak(a)


if __name__ == "__main__":
    main()
