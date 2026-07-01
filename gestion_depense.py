import csv
import pandas as pd
from datetime import datetime
from pathlib import Path

FICHIER = Path("depenses.csv")
COLONNES = ["date", "montant", "intitule", "categorie"]

# ------------------ AJOUT ------------------
def ajouter_depense():
    try:
        montant = float(input("Montant : "))
    except ValueError:
        print("Montant invalide.")
        return

    intitule = input("Intitulé : ").strip()
    categorie = input("Catégorie : ").strip().lower()

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

    print("Dépense ajoutée avec succès.")

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
def filtrer_depenses():
    categorie = input("Catégorie à filtrer : ").strip().lower()

    if not FICHIER.exists():
        print("Aucune dépense enregistrée.")
        return

    df = pd.read_csv(FICHIER)
    filtre = df[df["categorie"] == categorie]

    if filtre.empty:
        print("Aucune dépense pour cette catégorie.")
    else:
        print(filtre.to_string(index=True))

# ------------------ BALANCE ------------------
def calculer_balance():
    if not FICHIER.exists():
        print("Aucune dépense enregistrée.")
        return

    df = pd.read_csv(FICHIER)
    total = df["montant"].sum()

    print(f"Balance totale : {total:.2f} €")

# ------------------ SUPPRIMER ------------------
def supprimer_depense():
    if not FICHIER.exists():
        print("Aucune dépense enregistrée.")
        return

    df = pd.read_csv(FICHIER)
    print(df.to_string(index=True))

    try:
        index = int(input("Index à supprimer : "))
        df = df.drop(index).reset_index(drop=True)
        df.to_csv(FICHIER, index=False)
        print("Dépense supprimée.")
    except (ValueError, KeyError):
        print("Index invalide.")

# ------------------ MENU ------------------
def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Ajouter une dépense")
        print("2. Afficher les dépenses")
        print("3. Filtrer par catégorie")
        print("4. Calculer la balance")
        print("5. Supprimer une dépense")
        print("6. Quitter")

        choix = input("Choix : ")

        if choix == "1":
            ajouter_depense()
        elif choix == "2":
            afficher_depenses()
        elif choix == "3":
            filtrer_depenses()
        elif choix == "4":
            calculer_balance()
        elif choix == "5":
            supprimer_depense()
        elif choix == "6":
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    menu()
