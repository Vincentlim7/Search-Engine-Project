import re
import time
start_time = time.time()

#Renvoie true si text possede les mots voulus

def inCorpus(text):
    for word in text.split():
        if word.upper().startswith("SPORT"):
            return True

#Creer un nouveau fichier XML en gardant que les pages qui respecte inCorpus
#name_input : nom du fichier à traiter
#name_output : nom du nouveau fichier

def limitCorpus(name_input, name_output):
    outfile = open(name_output, 'w')
    text = ""
    n = 0
    
    with open(name_input, errors="ignore") as infile:
        copy = False
        for line in infile:
            if line.strip() == "<page>":
                copy = True
                text = text + line
                # Un progress bar en commentaire. Modifier le nombre si nécessaire (actuellement nombres de page dans frwiki)
                #n = n + 1
                #print(f'\r {n}/5321315', end = '\r')
                continue
            elif line.strip() == "</page>":
                copy = False
                text = text + line
                if(inCorpus(text)):
                    outfile.write(text)
                text = ""
                continue
            elif copy:
                text = text + line
    print('Terminé !')

# Compter le nombre de pages d'un fichier XML de wikipedia
# input : nom du fichier
# Il y a 5321315 pages different dans frwiki
# Il y a 429835 pages different dans wikilimit
# Il y a 22 pages different dans frwiki10000
# Il y a 11 pages different dans wikilimit10000

def nombresPages(input):
    n = 0
    with open(input, errors="ignore") as infile:
        for line in infile:
            if line.strip() == "<page>":
                n = n + 1
    return n

# Nettoyer le fichier xml et cree un nouveau fichier avec que les titre et text netoyé
# Le nouveau fichier transforme une page wikipedia en 4 lignes qui contient comme information dans l'ordre:
# id, titre original, titre nettoye et text nettoye
# On garde que les pages dont le text nettoye possède au moins size mots
# input : nom du fichier xml
# output : nom du nouveau fichier xml
# size : taille minimale du texte nettoye

def nettoyer_file(input, output, size):
    outfile = open(output, 'w', encoding="utf-8")
    with open(input, encoding="utf-8", errors="ignore") as infile:
        copy = False
        text = ""
        title = ""
        id = 0
        n = 0
        for line in infile:
            if "<title>" in line:  
                n += 1
                print(f'\r {n}/429835', end = '\r')
                title = re.sub(r' *</?title>', '', line)
            elif "<text bytes=" in line:
                tmp = line.split('>')
                text = text + tmp[1]
                copy = True
                continue
            elif "</text>" in line:
                text = text + line.replace('</text>','')
                copy = False
                text = nettoyer_text(text)
                if len(text.split()) >= size :
                    id += 1
                    outfile.write(str(id) + "\n")
                    outfile.write(title)
                    outfile.write(nettoyer_text(title) + "\n")
                    outfile.write(text + "\n")
                text = ""
                continue
            elif copy:
                text = text + line
    print(' ' + str(n))
    print('\nNombre de pages : ' + str(id))

# Nettoie les pages wikipedias selon certain critères :
# On enlève les sections innutile tel que Bibliographie
# Puis on enlèves les texts entre {| |}, {{ }} et [[ : ]] 
# On enlève les balises ref et tous les liens
# On enlève les caractères spéciaux, les chiffres et les espaces innutils
# Finalement on met tous en minuscule
# text : le text (string) qu'on veut nettoye

def nettoyer_text(text):
    text = supprimerSection(text)

    text = removeBetween(text, "{\|", "\|}")
    text = removeBetween(text, "{{", "}}")
    text = supprimerCrocher(text)

    text = re.sub(r'&lt;/?ref&gt;', ' ', text)
    text = re.sub(r'http\S+', ' ', text)

    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'[0-9]*', '', text)
    text = re.sub(' +', ' ', text)

    text = text.lower()
    return text

# Enlever certaines sections d'un article wikipedia
# Les sections supprimées sont "Notes et références", "Voir aussi", "Bibliographie" et "Annexes"
# text : le text où l'on veut supprimer des sections

def supprimerSection(text):
    result = ""
    copy = True
    for line in text.split('\n'):
        if line.startswith('== '):
            copy = True
        if line.strip() == "== Notes et références ==" or line.strip() == "== Voir aussi ==" or line.strip() == "== Bibliographie ==" or line.strip() == "== Annexes ==" or line.strip() == "== Articles connexes ==":
            copy = False
        elif copy :
            result += line + '\n'
    return result

# Enlever les mots entre deux strings (exemple les parentheses). Prend en compte les cas embrique
# text : le text où l'on veut supprimer des mots
# start : le début de la suppression
# end : fin de la suppression
# Si on veut garder les \n, utiliser le for mis en commentaire

def removeBetween(text, start, end):
    result = ''
    skip = 0
    text = re.sub(start, ' ' + start + ' ', text)
    text = re.sub(end, ' ' + end + ' ', text)
    for mot in text.split() :
    #for mot in re.findall(r'\S+|\n',text):
        if start in mot:
            skip += 1
        elif end in mot and skip > 0:
            skip -= 1
        elif skip == 0:
            result += mot + " "
    return result

# Supprimer entre [[]] s'il y a : dans les crochet
# text : le text où l'on veut supprimer des mots

def supprimerCrocher(text):
    result = ''
    entre = ''
    doubleP = False
    skip = 0
    text = re.sub('\[\[', ' [[ ', text)
    text = re.sub('\]\]', ' ]] ', text)
    for mot in text.split():
    #for mot in re.findall(r'\S+|\n',text):
        if '[[' in mot:
            entre += mot + " "
            skip += 1
        elif ']]' in mot and skip > 1:
            entre += mot + " "
            skip -= 1
        elif ']]' in mot and skip == 1:
            entre += mot + " "
            skip -= 1
            if not doubleP:
                result += entre
            doubleP = False
            entre = ''
        elif skip > 0:
            entre += mot + " "
            if ':' in mot:
                doubleP = True
        elif skip == 0:
            result += mot + " "
    return result

# print(nombresPages('wikilimit.xml'))
 
#limitCorpus('frwiki.xml','wikilimit.xml')             
#limitCorpus('frwiki10000.xml','wikilimit10000.xml')


nettoyer_file('wikilimit.xml', 'wikinettoye.xml', 200)
#nettoyer_file('wikilimit10000.xml', 'wikinettoye10000.xml', 1000)

# 1000 - 57896 - 1953s
# 500 - 103711 - 1919s
# 300 - 151408 - 1976s
# 250 - 170710 - 2003s
# 200 - 195077 - 1968s

print("--- %s seconds ---" % (time.time() - start_time))