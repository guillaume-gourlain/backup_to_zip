# backup_to_zip

Mini-outil Python de sauvegarde versionnée d’un dossier au format ZIP.

Le script crée automatiquement une archive ZIP numérotée sans écraser les sauvegardes précédentes.
Exemple : si `dates_1.zip` et `dates_2.zip` existent déjà, la sauvegarde suivante sera créée sous le nom `dates_3.zip`.

## Objectif

Ce projet sert à automatiser une tâche simple mais fréquente : sauvegarder un dossier de travail dans une archive ZIP, tout en évitant les écrasements silencieux.

Il met en pratique plusieurs mécanismes importants :

* validation d’un dossier source ;
* création automatique d’un dossier `sauvegardes` ;
* numérotation automatique des archives ;
* parcours récursif avec `os.walk()` ;
* création d’archives avec `zipfile`;
* chemins internes propres grâce à `os.path.relpath()`;
* exclusion des anciennes archives ZIP du dossier source ;
* tests de validation dans un bac à sable.

## Structure du projet

```text
backup_to_zip.py
demo_backup_to_zip.py
README.md
```

### `backup_to_zip.py`

Contient la fonction principale :

```python
backup_to_zip(dossier_source)
```

Elle reçoit le chemin d’un dossier source et retourne le chemin de l’archive ZIP créée.

### `demo_backup_to_zip.py`

Contient :

* la création du bac à sable ;
* les fonctions de test ;
* l’inspection du contenu de l’archive ;
* le lancement de la démonstration.

## Exemple d’utilisation

```python
from backup_to_zip import backup_to_zip

chemin_archive = backup_to_zip("chemin/vers/mon_dossier")
print("Archive créée :", chemin_archive)
```

Si le dossier source s’appelle `dates`, le script crée les archives dans un dossier `sauvegardes` placé au même niveau que `dates`.

Exemple :

```text
demo_backup_to_zip/
└── backup_demo/
    ├── dates/
    │   ├── notes.txt
    │   ├── rapport.txt
    │   ├── documents/
    │   │   ├── contrat.pdf
    │   │   └── facture.txt
    │   └── images/
    │       └── photo.jpg
    └── sauvegardes/
        ├── dates_1.zip
        ├── dates_2.zip
        └── dates_3.zip
```

## Tests réalisés

La version actuelle est validée avec une batterie de tests sur bac à sable.

Tests couverts :

1. Bac à sable créé correctement.
2. Source absente refusée proprement.
3. Source existante mais non dossier refusée proprement.
4. Première sauvegarde créée sans écrasement.
5. Contenu interne de l’archive propre.
6. Anciennes archives ZIP exclues du contenu final.
7. Relance stable avec création de l’archive suivante.

Extrait de sortie terminal :

```text
--- TESTS BACKUP TO ZIP ---
Statut bac à sable : créé.

--- TEST 1 : BAC A SABLE ---
Test bac à sable : OK

--- TEST 2 : SOURCE ABSENTE ---
REFUS : source absente.
Test source absente : OK

--- TEST 3 : SOURCE = FICHIER ---
REFUS : la source existe mais ce n'est pas un dossier.
Test source fichier : OK

--- TEST 4 ET 7 : CREATION + RELANCE ---
Première archive créée : .../sauvegardes/dates_3.zip
Deuxième archive créée : .../sauvegardes/dates_4.zip
Test création + relance : OK

Test contenu archive : OK

--- BILAN FINAL ---
Tous les tests sont validés.
```

## Sécurité

Le cœur du script ne supprime aucun fichier utilisateur.

La fonction de démonstration utilise `shutil.rmtree()` uniquement pour réinitialiser un bac à sable de test contrôlé.
Cette suppression ne doit jamais être utilisée automatiquement sur un dossier réel fourni par un utilisateur.

Le script vérifie aussi que la source existe et qu’il s’agit bien d’un dossier avant de créer une archive.

## Limites actuelles

Cette version est une démonstration portfolio V1, pas encore un outil client-ready.

Limites connues :

* pas d’interface en ligne de commande ;
* pas de fichier de configuration ;
* pas de logs persistants ;
* pas de choix utilisateur pour le dossier de sortie ;
* pas de filtre avancé par extension ;
* pas de tests unitaires avec un framework comme `unittest` ou `pytest`.

## Améliorations possibles

Évolutions envisageables :

* ajouter une interface CLI simple ;
* permettre de choisir le dossier de destination des sauvegardes ;
* ajouter un mode dry run ;
* écrire un journal de sauvegarde ;
* ajouter des tests automatisés avec `pytest` ;
* permettre d’exclure certains dossiers ou extensions ;
* créer une version utilisable sur des cas métier réels.

## Statut

Portfolio V1 — démonstration sécurisée et testée.

Le projet montre un flux complet : validation de la source, sauvegarde versionnée, parcours récursif, création ZIP, exclusions, inspection et batterie de tests.
