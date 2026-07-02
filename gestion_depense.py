import argparse
import csv
import sys
import pandas as pd
from datetime import datetime
from pathlib import Path

FICHIER = Path("depenses.csv")
COLONNES = ["date", "montant", "intitule", "categorie"]

# ------------------ AJOUT ------------------
def ajouter_depense(montant, intitule, categorie):
    intitule = intitule.strip()
    categorie = categorie.strip().lower()

    nouvelle_depense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "montant": montant,
        "intitule": intitule,
        "categorie": categorie
    }

    fichier_existe = FICHIER.exists()

    with FICHIER.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLONNES)
        if not fichier_existe:
            writer.writeheader()
        writer.writerow(nouvelle_depense)

    print("Dépense ajoutée :", montant, "€")

# ------------------ AFFICHER ------------------
def afficher_depenses():
    if not FICHIER.exists():
        print("Aucune dépense enregistrée.")
        return

    df = pd.read_csv(FICHIER)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date")

    print(df.to_string(index=True))

# ------------------ FILTRER ------------------
def filtrer_depenses(categorie):
    categorie = categorie.strip().lower()

    if not FICHIER.exists():
        print("Aucune dépense.")
        return

    df = pd.read_csv(FICHIER)
    filtre = df[df["categorie"] == categorie]

    if filtre.empty:
        print("Aucune dépense trouvée.")
    else:
        print(filtre.to_string(index=True))

# ------------------ BALANCE ------------------
def calculer_balance():
    if not FICHIER.exists():
        print("Aucune dépense.")
        return

    df = pd.read_csv(FICHIER)
    total = df["montant"].sum()

    print("Total :", total, "€")
# ------------------ SUPPRIMER ------------------
def supprimer_depense(index):
    if not FICHIER.exists():
        print("Aucune dépense.")
        return

    df = pd.read_csv(FICHIER)

    if index not in df.index:
        print("Index invalide.")
        return

    df = df.drop(index).reset_index(drop=True)
    df.to_csv(FICHIER, index=False)

    print("Dépense supprimée.")

# système de lecture des commandes terminal
def construire_parser():
    parser = argparse.ArgumentParser()
   # Sous-commandes du programme
    sub = parser.add_subparsers(dest="commande", required=True)

    add = sub.add_parser("ajouter")
    add.add_argument("montant", type=float)
    add.add_argument("intitule")
    add.add_argument("categorie")

    sub.add_parser("afficher")

    fil = sub.add_parser("filtrer")
    fil.add_argument("categorie")

    sub.add_parser("balance")

    sup = sub.add_parser("supprimer")
    sup.add_argument("index", type=int)

    return parser


def main():
    parser = construire_parser()
    args = parser.parse_args()

    try:
        if args.commande == "ajouter":
            ajouter_depense(args.montant, args.intitule, args.categorie)
        elif args.commande == "afficher":
            afficher_depenses()
        elif args.commande == "filtrer":
            filtrer_depenses(args.categorie)
        elif args.commande == "balance":
            calculer_balance()
        elif args.commande == "supprimer":
            supprimer_depense(args.index)
    except ValueError:
        print("Erreur de valeur")
        sys.exit(1)


if __name__ == "__main__":
    main()
