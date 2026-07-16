# demo_backup_to_zip.py
# Démonstration et tests pour backup_to_zip.py
# Statut : Portfolio V1 — démonstration sécurisée et testée
#
# Contenu :
# - création d'un bac à sable contrôlé
# - tests source absente / source fichier
# - test de sauvegarde versionnée
# - inspection du contenu ZIP
# - vérification des chemins internes
# - vérification de l'exclusion des anciennes archives ZIP
#
# Sécurité :
# shutil.rmtree() est utilisé uniquement pour réinitialiser
# le bac à sable de démonstration.


import os
import zipfile
import shutil

from backup_to_zip import backup_to_zip


def creer_bac_a_sable():
    racine = "demo_backup_to_zip"

    dossier_source = os.path.join(
        racine,
        "backup_demo"
    )

    # ATTENTION : rmtree() est utilisé uniquement pour réinitialiser
    # le bac à sable de démonstration. Ne jamais l'utiliser dans backup_to_zip().
    if os.path.exists(dossier_source):
        shutil.rmtree(dossier_source)

    os.makedirs(dossier_source, exist_ok=True)

    dossier_dates = os.path.join(
        dossier_source,
        'dates'
    )

    os.makedirs(dossier_dates, exist_ok=True)

    noms_fichiers_dates = [
        'notes.txt',
        'rapport.txt',
        'dates_99.zip'
    ]

    for nom_fichier in noms_fichiers_dates:
        chemin = os.path.join(dossier_dates, nom_fichier)

        with open(chemin, 'w', encoding='utf-8') as fichier:
            fichier.write("Test")

    dossier_documents = os.path.join(
        dossier_dates,
        'documents'
    )

    os.makedirs(dossier_documents, exist_ok=True)

    noms_fichiers_documents = [
        'facture.txt',
        'contrat.pdf'
    ]

    for nom_fichier in noms_fichiers_documents:
        chemin = os.path.join(dossier_documents, nom_fichier)
        
        with open(chemin, "w", encoding='utf-8') as fichier:
            fichier.write('test')

    dossier_images = os.path.join(
        dossier_dates,
        'images'
    )

    os.makedirs(dossier_images, exist_ok=True)

    nom_fichier_image = 'photo.jpg'
    
    chemin = os.path.join(dossier_images, nom_fichier_image)

    with open(chemin, 'w', encoding='utf-8') as fichier :
        fichier.write('test')

    dossier_sauvegardes = os.path.join(
        dossier_source,
        'sauvegardes'
    )

    os.makedirs(dossier_sauvegardes, exist_ok=True)

    noms_fichiers_sauvegardes = [
        'dates_1.zip',
        'dates_2.zip'
    ]

    for nom_fichier in noms_fichiers_sauvegardes:
        chemin = os.path.join(dossier_sauvegardes, nom_fichier)

        with open(chemin, 'w', encoding='utf-8') as fichier:
            fichier.write('test')
    
    print('Statut bac à sable : créé.')

    return dossier_dates


def inspecter_archive(chemin_archive):
    if chemin_archive is None:
        print("Inspection impossible : aucune archive créée.")
        return []

    if not os.path.isfile(chemin_archive):
        print("Inspection impossible : archive introuvable.")
        return []

    with zipfile.ZipFile(chemin_archive, "r") as archive_zip:
        contenu = archive_zip.namelist()

    print()
    print("Contenu de l'archive :")
    for nom_interne in contenu:
        print("-", nom_interne)

    return contenu


def verifier_contenu_archive(contenu):
    attendus = [
        "dates/",
        "dates/notes.txt",
        "dates/rapport.txt",
        "dates/documents/",
        "dates/documents/contrat.pdf",
        "dates/documents/facture.txt",
        "dates/images/",
        "dates/images/photo.jpg",
    ]

    interdits = [
        "dates/dates_99.zip",
        "sauvegardes/dates_1.zip",
        "sauvegardes/dates_2.zip",
        "sauvegardes/dates_3.zip",
        "sauvegardes/dates_4.zip",
    ]

    contenu_set = set(contenu)

    test_attendus = True
    for nom in attendus:
        if nom not in contenu_set:
            print("ERREUR - élément attendu absent :", nom)
            test_attendus = False

    test_interdits = True
    for nom in interdits:
        if nom in contenu_set:
            print("ERREUR - élément interdit présent :", nom)
            test_interdits = False

    test_chemins_absolus = True
    for nom in contenu:
        if ":" in nom or nom.startswith("/") or nom.startswith("\\"):
            print("ERREUR - chemin absolu détecté :", nom)
            test_chemins_absolus = False

    if test_attendus and test_interdits and test_chemins_absolus:
        print("Test contenu archive : OK")
        return True

    print("Test contenu archive : ECHEC")
    return False


def tester_bac_a_sable(dossier_dates):
    print()
    print("--- TEST 1 : BAC A SABLE ---")

    parent_source = os.path.dirname(dossier_dates)
    dossier_sauvegardes = os.path.join(parent_source, "sauvegardes")

    chemins_attendus = [
        dossier_dates,
        os.path.join(dossier_dates, "notes.txt"),
        os.path.join(dossier_dates, "rapport.txt"),
        os.path.join(dossier_dates, "dates_99.zip"),
        os.path.join(dossier_dates, "documents"),
        os.path.join(dossier_dates, "documents", "facture.txt"),
        os.path.join(dossier_dates, "documents", "contrat.pdf"),
        os.path.join(dossier_dates, "images"),
        os.path.join(dossier_dates, "images", "photo.jpg"),
        dossier_sauvegardes,
        os.path.join(dossier_sauvegardes, "dates_1.zip"),
        os.path.join(dossier_sauvegardes, "dates_2.zip"),
    ]

    test_ok = True

    for chemin in chemins_attendus:
        if not os.path.exists(chemin):
            print("ERREUR - élément absent :", chemin)
            test_ok = False

    if test_ok:
        print("Test bac à sable : OK")
        return True

    print("Test bac à sable : ECHEC")
    return False


def tester_source_absente(dossier_reference):
    print()
    print("--- TEST 2 : SOURCE ABSENTE ---")

    parent = os.path.dirname(dossier_reference)
    chemin_absent = os.path.join(parent, "dossier_absent")

    resultat = backup_to_zip(chemin_absent)

    if resultat is None:
        print("Test source absente : OK")
        return True

    print("Test source absente : ECHEC")
    return False


def tester_source_fichier(dossier_reference):
    print()
    print("--- TEST 3 : SOURCE = FICHIER ---")

    parent = os.path.dirname(dossier_reference)
    chemin_fichier = os.path.join(parent, "source_fichier.txt")

    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        fichier.write("test")

    resultat = backup_to_zip(chemin_fichier)

    if resultat is None:
        print("Test source fichier : OK")
        return True

    print("Test source fichier : ECHEC")
    return False


def tester_creation_et_relance(dossier_source):
    print()
    print("--- CREATION + RELANCE SANS ECRASEMENT ---")

    chemin_archive_1 = backup_to_zip(dossier_source)
    chemin_archive_2 = backup_to_zip(dossier_source)

    test_ok = True

    if chemin_archive_1 is None:
        print("ERREUR - première archive non créée.")
        test_ok = False
    elif not os.path.isfile(chemin_archive_1):
        print("ERREUR - première archive introuvable :", chemin_archive_1)
        test_ok = False
    elif os.path.basename(chemin_archive_1) != "dates_3.zip":
        print("ERREUR - première archive attendue : dates_3.zip")
        print("Archive obtenue :", chemin_archive_1)
        test_ok = False
    else:
        print("Première archive créée :", chemin_archive_1)

    if chemin_archive_2 is None:
        print("ERREUR - deuxième archive non créée.")
        test_ok = False
    elif not os.path.isfile(chemin_archive_2):
        print("ERREUR - deuxième archive introuvable :", chemin_archive_2)
        test_ok = False
    elif os.path.basename(chemin_archive_2) != "dates_4.zip":
        print("ERREUR - deuxième archive attendue : dates_4.zip")
        print("Archive obtenue :", chemin_archive_2)
        test_ok = False
    else:
        print("Deuxième archive créée :", chemin_archive_2)

    if test_ok:
        print("Test création + relance : OK")
    else:
        print("Test création + relance : ECHEC")

    return test_ok, chemin_archive_2


def main():

    print("--- TESTS BACKUP TO ZIP ---")

    dossier_dates = creer_bac_a_sable()

    test_bac = tester_bac_a_sable(dossier_dates)
    test_absente = tester_source_absente(dossier_dates)
    test_fichier = tester_source_fichier(dossier_dates)

    test_creation, derniere_archive = tester_creation_et_relance(dossier_dates)

    contenu = inspecter_archive(derniere_archive)
    test_contenu = verifier_contenu_archive(contenu)

    print()
    print("--- BILAN FINAL ---")

    resultats = [
        test_bac,
        test_absente,
        test_fichier,
        test_creation,
        test_contenu,
    ]

    if all(resultats):
        print("Tous les tests sont validés.")
    else:
        print("Au moins un test a échoué.")

if __name__ == "__main__":
    main()
