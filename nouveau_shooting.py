#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cree un nouveau shooting (nouvelle campagne) pret a recevoir des enfants.

Usage :
    python nouveau_shooting.py assmat-2027 "Shooting Assistantes Maternelles 2027"

Le dossier cree contient :
  index.html        (meme moteur que le shooting 2026)
  config.json       (titre + tarifs + moyens de paiement)
  generer_liens.py  (genere enfants.json + LIENS.txt + dossiers photos/)
  enfants.txt       (a remplir : "Prenom | Assmat", une ligne par enfant)
  photos/           (photos/<code>/1.jpg, 2.jpg ...)

Les tarifs et les liens de paiement sont recopies depuis le config.json du dossier parent.
"""
import json, os, shutil, sys

RACINE = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    slug = sys.argv[1].strip().strip('/')
    titre = sys.argv[2].strip() if len(sys.argv) > 2 else "Shooting " + slug

    dest = os.path.join(RACINE, slug)
    if os.path.exists(dest):
        print("Le dossier existe deja :", dest)
        sys.exit(1)

    os.makedirs(dest)
    os.makedirs(os.path.join(dest, "photos"))

    # 1. moteur de page
    shutil.copy(os.path.join(RACINE, "index.html"), os.path.join(dest, "index.html"))
    shutil.copy(os.path.join(RACINE, "generer_liens.py"), os.path.join(dest, "generer_liens.py"))

    # 2. config : on part de celle du parent (memes tarifs), on change le titre
    cfg_parent = {}
    p = os.path.join(RACINE, "config.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            cfg_parent = json.load(f)
    cfg = {
        "titre": titre,
        "photo": cfg_parent.get("photo", {"prix": 12, "pack": 30, "packN": 3}),
        "tarifs": cfg_parent.get("tarifs", {}),
        "paiement": cfg_parent.get("paiement", {})
    }
    cfg["paiement"]["revolut"] = ""  # a remplir avec le lien Revolut
    with open(os.path.join(dest, "config.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    # 3. liste d'enfants vide
    with open(os.path.join(dest, "enfants.txt"), "w", encoding="utf-8") as f:
        f.write("# Prenom | Assistante maternelle\n")

    print("Cree :", dest)
    print("1. remplir enfants.txt")
    print("2. mettre les photos dans photos/<code>/1.jpg ...")
    print("3. python generer_liens.py https://kensy01.github.io/prycilia-shooting-2026/" + slug)


if __name__ == "__main__":
    main()
