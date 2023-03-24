with open("data/pages/wikiprocess.txt", "r") as f_in:
    with open("data/pages/test2.txt", "w") as f_out:
        for i, line in enumerate(f_in):
            # Si la ligne est la première d'un bloc de 5 lignes
            if i % 5 == 0:
                # Récupérer le page_id
                page_id = int(line.strip())
                # Soustraire 1 à page_id
                page_id -= 1
                # Écrire la nouvelle première ligne avec page_id - 1
                f_out.write(str(page_id) + "\n")
            # Si la ligne n'est pas la première ou la deuxième d'un bloc de 5 lignes
            else:
                # Écrire la ligne telle quelle
                f_out.write(line)

# Écraser le fichier d'origine avec le contenu modifié
import os
os.replace("data/pages/test2.txt", "data/pages/wikiprocess.txt")