#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Génère les liens personnalisés par enfant pour le shooting PryciliaShad 2026.

UTILISATION
    1. Écris les prénoms dans enfants.txt (un par ligne)
    2. python generer_liens.py https://ton-site.netlify.app
       (sans URL, les liens seront relatifs → test en local)

RÉSULTAT
    - enfants.json   : la config lue par index.html
    - LIENS.txt      : un lien prêt à copier-coller par enfant
    - photos/<code>/ : dossier où déposer 1.jpg, 2.jpg, 3.jpg
"""
import json, re, sys, unicodedata, secrets
from pathlib import Path

BASE = Path(__file__).parent
URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ""

def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "enfant"

def main():
    src = BASE / "enfants.txt"
    if not src.exists():
        src.write_text("Lucien\nMila\nNoah\n", encoding="utf-8")
        print("→ enfants.txt créé avec 3 exemples. Modifie-le puis relance.")
        return

    prenoms = []
    for l in src.read_text(encoding="utf-8").splitlines():
        l = l.strip()
        if not l:
            continue
        nom, _, assmat = [x.strip() for x in l.partition("|")]
        prenoms.append((nom, assmat or None))
    ancien = {}
    jf = BASE / "enfants.json"
    if jf.exists():
        try:
            for e in json.loads(jf.read_text(encoding="utf-8")).get("enfants", []):
                ancien[e["prenom"].lower()] = e["code"]      # on garde les codes déjà envoyés
        except Exception:
            pass

    enfants, lignes = [], []
    EXTS = {".jpg", ".jpeg", ".png", ".webp"}
    for p, assmat in prenoms:
        code = ancien.get(p.lower()) or f"{slug(p)}-{secrets.token_hex(2)}"
        d = BASE / "photos" / code
        d.mkdir(parents=True, exist_ok=True)
        trouvees = sorted((f.name for f in d.iterdir() if f.suffix.lower() in EXTS),
                          key=lambda n: (len(n), n))
        photos = [f"photos/{code}/{n}" for n in trouvees] or \
                 [f"photos/{code}/{i}.jpg" for i in (1, 2, 3)]
        e = {"prenom": p, "code": code, "photos": photos}
        if assmat:
            e["assmat"] = assmat
        enfants.append(e)
        lien = f"{URL}/index.html?e={code}" if URL else f"index.html?e={code}"
        lignes.append(f"{p:<18} {lien}   ({len(trouvees)} photo(s))")

    cfg = {"marque": "PryciliaShad Photographie", "whatsapp": "33659117114", "enfants": enfants}
    jf.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "LIENS.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")

    print(f"{len(enfants)} enfant(s) — enfants.json et LIENS.txt écrits.\n")
    print("\n".join(lignes))
    print("\nDépose maintenant les photos dans photos/<code>/ : 1.jpg, 2.jpg, 3.jpg")

if __name__ == "__main__":
    main()
