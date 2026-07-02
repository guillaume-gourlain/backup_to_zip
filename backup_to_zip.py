import os
import zipfile


def backup_to_zip(dossier_source):
    """
    Crée une archive ZIP versionnée d'un dossier source.

    L'archive est créée dans un dossier "sauvegardes" placé au même niveau
    que le dossier source. Les archives existantes ne sont pas écrasées :
    le script cherche automatiquement le premier numéro disponible.

    Exemple :
    dates_1.zip, dates_2.zip existent déjà -> création de dates_3.zip.

    Retourne le chemin de l'archive créée.
    Retourne None si la source est absente ou si ce n'est pas un dossier.
    """
    dossier_source = os.path.abspath(dossier_source)

    if not os.path.exists(dossier_source):
        print("REFUS : source absente.")
        return None

    if not os.path.isdir(dossier_source):
        print("REFUS : la source existe mais ce n'est pas un dossier.")
        return None

    parent_source = os.path.dirname(dossier_source)
    nom_dossier_source = os.path.basename(dossier_source)

    dossier_sauvegardes = os.path.join(parent_source, "sauvegardes")
    os.makedirs(dossier_sauvegardes, exist_ok=True)

    numero = 1

    while True:
        nom_archive = f"{nom_dossier_source}_{numero}.zip"
        chemin_archive = os.path.join(dossier_sauvegardes, nom_archive)

        if not os.path.exists(chemin_archive):
            break

        numero += 1

    with zipfile.ZipFile(chemin_archive, "w", zipfile.ZIP_DEFLATED) as archive_zip:
        for foldername, _subfolders, filenames in os.walk(dossier_source):
            nom_dossier_interne = os.path.relpath(foldername, parent_source)
            archive_zip.write(foldername, nom_dossier_interne)

            for filename in filenames:
                if filename.startswith(nom_dossier_source + "_") and filename.endswith(".zip"):
                    continue

                chemin_fichier = os.path.join(foldername, filename)
                nom_fichier_interne = os.path.relpath(chemin_fichier, parent_source)

                archive_zip.write(chemin_fichier, nom_fichier_interne)

    return chemin_archive