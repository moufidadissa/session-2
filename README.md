# Rendu session 2

## Projet : Gestionnaire de Dépenses
<


- **Nom 
  - Adissa Moufid — 202463680

---

## Objectif du projet

Ce projet a pour but de créer un outil qui permet d’enregistrer les dépenses d’une personne.
Chaque dépense a :

- une somme (positive ou négative),
- un intitulé (description),
- une catégorie (ex : alimentation, transport, salaire...).

Les dépenses sont sauvegardées dans un fichier CSV avec la date et la balance totale mise à jour.

---

## Fonctionnalités du noyau minimal (indispensables)

1. **Ajouter une dépense**
   - Saisir la somme, l’intitulé et la catégorie.
   - Enregistrer la dépense dans le fichier CSV.
   - Calculer automatiquement la nouvelle balance.

2. **Afficher les dépenses enregistrées**
   - Lire le fichier CSV et afficher la liste triée par date.

3. **Calcul de la balance totale**
   - Calcul automatique après chaque ajout.

---

## Fonctionnalités supplémentaires (optionnelles)

4.**Filtrer les dépenses**
  -Proposer automatiquement les catégories déjà utilisées.

5.**Suppression d’une dépense**
   -Permettre de retirer une dépense du fichier CSV.

---

## Dépendances entre les fonctionnalités

| Fonctionnalité | Dépend de |
|----------------|------------|
| 1. Ajouter une dépense | aucune |
| 2. Afficher les dépenses | #1 |
| 3. Calculer la balance totale | #1 |
| 6. Filtrer les dépenses | #2 |
| 5. Supprimer une dépense | #1 |

---

## Priorités

 1. **Noyau minimal :** fonctionnalités 1, 2 et 3  
 2. **Améliorations :** fonctionnalités 4 à 7.

## Rendu 2

## Fonctionnalités et choix des briques logicielles

---

### 1 Ajouter une dépense

**Objectif :**  
Saisir la somme, l’intitulé, la catégorie et enregistrer le tout dans un fichier CSV, avec la date et la balance mise à jour.

**Modules Python standard :**

| Module      | Service rendu                                   | Limites                                     |
|-------------|--------------------------------------------------|---------------------------------------------|
| `csv`       | Lire et écrire facilement dans un fichier CSV.  | Gestion manuelle des erreurs et conversions. |
| `datetime`  | Enregistrer automatiquement la date du jour.    | Formatage manuel nécessaire.                |
| `pathlib`   | Gestion moderne et lisible des chemins de fichiers. | Ne gère pas la logique métier.             |
| `argparse`  | Permet de récupérer des arguments en ligne de commande pour ajouter une dépense. | Nécessite plus de code qu’un module tiers. |

**Modules tiers :**

| Module   | Service rendu                                      | Limites                               |
|----------|---------------------------------------------------|----------------------------------------|
| `pandas` | Manipulation simple de tableaux, lecture/écriture CSV. | Plus lourd à installer, syntaxe spécifique. |

**Outils externes :**

| Outil                     | Service rendu                           | Limites                             |
|---------------------------|------------------------------------------|-------------------------------------|
| LibreOffice Calc / Excel | Création manuelle de CSV pour tests.     | Non automatisé, externe au projet.  |

**Analyse :**

- Facilité d’installation : tous les modules standards sont déjà disponibles.  
- `argparse` permet une interface claire en ligne de commande pour l’utilisateur.  
- `pathlib` rend la gestion des fichiers plus simple et portable.  
- `pandas` est puissant mais optionnel pour le noyau minimal.

---

### 2 Afficher les dépenses

**Objectif :** Lire le fichier CSV et afficher la liste triée par date.

**Modules standard :**

| Module      | Service rendu                                  | Limites                     |
|-------------|-------------------------------------------------|-----------------------------|
| `csv`       | Lecture ligne par ligne.                        | Tri manuel obligatoire.     |
| `datetime`  | Permet de comparer les dates.                   | Plus complexe à coder.      |
| `pathlib`   | Vérification de l’existence du fichier CSV.     | Pas de traitement de données. |

**Modules tiers :**

| Module     | Service rendu                                                | Limites           |
|------------|---------------------------------------------------------------|------------------|
| `pandas`   | Lecture CSV + tri en une ligne : `df.sort_values("Date")`.    | Dépendance tierce |
| `rich`     | Affichage amélioré (tableaux colorés) dans le terminal.       | Purement visuel   |

**Analyse :**  
`pandas` + `rich` = affichage simple, lisible et tri rapide.  
Solution totalement réalisable sans module tiers pour le noyau minimal.

---

### 3 Calculer la balance totale

**Objectif :** Faire la somme automatique des montants après chaque ajout.

| Module   | Service rendu                               | Limites                   |
|----------|----------------------------------------------|---------------------------|
| `csv`    | Parcours des lignes et addition des montants. | Long à coder, peu flexible. |
| `pandas` | Calcul direct : `df["Montant"].sum()`.        | Installation nécessaire.  |

**Analyse :**

- Avec `csv`, cela fonctionne mais est moins pratique.  
- Avec `pandas`, c’est quasi instantané.

---

### 4 Filtrer les dépenses

**Objectif :** Afficher uniquement certaines dépenses selon une catégorie, une date ou un montant.

| Module            | Service rendu                                             | Limites                             |
|-------------------|------------------------------------------------------------|-------------------------------------|
| `csv + datetime`  | Filtrage manuel des lignes selon conditions.               | Très long à maintenir.              |
| `pandas`          | Filtrage simple : `df[df["Catégorie"] == "Transport"]`.    | Requiert installation.              |
| `argparse`        | Permet d’ajouter des options CLI : `--categorie`, `--date`. | Ne filtre pas, sert juste à récupérer l’info. |

**Analyse :**

- `argparse` = interface en ligne de commande pour choisir le filtre.  
- `pandas` = moteur de filtrage rapide et fiable.  

---

### 5 Supprimer une dépense

**Objectif :** Permettre de retirer une dépense du fichier CSV.

| Module   | Service rendu                                   | Limites                                     |
|----------|--------------------------------------------------|---------------------------------------------|
| `csv`    | Réécriture du fichier sans la ligne supprimée.   | Très manuel et fastidieux.                  |
| `pandas` | Suppression via `df.drop(index)` puis `to_csv()`. | Besoin d’un identifiant unique.             |

**Analyse :**  
`pandas` rend la suppression plus simple et plus propre.  
La méthode standard `csv` reste faisable mais lourde.

---

### Analyse transversale (vue d’ensemble)

| Critère                | Bibliothèque standard | Bibliothèques tierces | Outils externes |
|------------------------|--------------------|--------------------|----------------|
| Facilité d’installation | Aucune installation requise | `pip install` simple | Déjà installés (souvent) |
| Facilité d’utilisation | Plus de code à écrire | Syntaxe simple et moderne | Pas intégrés à Python |
| Compatibilité           | Totale             | Très bonne         | Dépend du système |
| Maintenance / communauté| Stable mais basique | Excellentes (pandas, typer, rich) | Variable |
| Documentation           | Bonne              | Très bonne         | Limitée à l’outil |
| Performances            | Correctes          | Très bonnes pour gros fichiers | Hors du code |

