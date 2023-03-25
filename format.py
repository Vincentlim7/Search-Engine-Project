## REMAP PAGE ID STARTING FROM 0 INSTEAD OF 1

# with open("data/pages/wikiprocess.txt", "r") as f_in:
#     with open("data/pages/test2.txt", "w") as f_out:
#         for i, line in enumerate(f_in):
#             # Si la ligne est la première d'un bloc de 5 lignes
#             if i % 5 == 0:
#                 # Récupérer le page_id
#                 page_id = int(line.strip())
#                 # Soustraire 1 à page_id
#                 page_id -= 1
#                 # Écrire la nouvelle première ligne avec page_id - 1
#                 f_out.write(str(page_id) + "\n")
#             # Si la ligne n'est pas la première ou la deuxième d'un bloc de 5 lignes
#             else:
#                 # Écrire la ligne telle quelle
#                 f_out.write(line)

# # Écraser le fichier d'origine avec le contenu modifié
# import os
# os.replace("data/pages/test2.txt", "data/pages/wikiprocess.txt")


## DELETING PAGE ID IN LINKS THAT ARE HIGHER THAN MAX(PAGE ID)

# threshold = 195077
# with open('./data/pages/wikiprocess.txt', 'r') as file, open('./data/pages/wikiprocessnew.txt', 'w') as new_file:
#     # Utilise islice pour extraire chaque bloc de 5 lignes
#     for line_nb, line in enumerate(file, 1):
#         if line_nb < 5:
#             if line_nb % 4 == 0:
#                 values = line.split()
#                 filtered_values = [value for value in values if int(value) < threshold]
#                 filtered_line = ' '.join(filtered_values)
#                 new_file.write(filtered_line + '\n')
            
#             else:
#                 new_file.write(line)
#         else:
#             if (line_nb-4) % 5 == 0:
#                 values = line.split()
#                 filtered_values = [value for value in values if int(value) < threshold]
#                 filtered_line = ' '.join(filtered_values)
#                 new_file.write(filtered_line + '\n')
            
#             else:
#                 new_file.write(line)

# print('Le nouveau fichier a été créé avec succès.')


## COMPUTE TITLE MAP

# page_id = 0
# title_map = dict()
# with open("./data/pages/wikiprocess.txt", 'r') as file:
#     for line in islice(file, 1, None, 5):
#         line = line.rstrip()
#         title_map[page_id] = line
#         page_id+=1

# with open('data/title_map.pickle', 'wb') as f:
#     pickle.dump(title_map, f, pickle.HIGHEST_PROTOCOL)