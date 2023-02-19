import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from spellchecker import SpellChecker
import spacy
import fr_core_news_md
import re
import time

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
                # Un progress bar 
                n = n + 1
                print(f'\r {n}/5321315', end = '\r')
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
        id_link = {}
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
                text, links = nettoyer_text(text)
                if len(text.split()) >= size :
                    id += 1
                    id_link[title.split('\n')[0]] = id
                    outfile.write(str(id) + "\n")
                    outfile.write(title)
                    outfile.write(nettoyer_text(title)[0] + "\n")
                    outfile.write(links + "\n")
                    outfile.write(text + "\n")
                text = ""
                continue
            elif copy:
                text = text + line
    print(' ' + str(n))
    print('\nNombre de pages : ' + str(id))
    return id_link

# Nettoie les pages wikipedias selon certain critères :
# On enlève les sections innutile tel que Bibliographie
# Puis on enlèves les texts entre {| |}, {{ }} et [[ : ]] 
# On enlève les balises ref et tous les liens
# On enlève les caractères spéciaux, les chiffres et les espaces innutils
# Finalement on met tous en minuscule
# On renvoie aussi la liste des liens internes obtenue grâce à supprimerCrocher
# text : le text (string) qu'on veut nettoye

def nettoyer_text(text):
    text, links = supprimerCrocher(text)
    text = supprimerSection(text)

    text = removeBetween(text, "{\|", "\|}")
    text = removeBetween(text, "{{", "}}")
    # text, links = supprimerCrocher(text)

    text = re.sub(r'&lt;/?ref&gt;', ' ', text)
    text = re.sub(r'http\S+', ' ', text)

    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'[0-9]*', '', text)
    text = re.sub(' +', ' ', text)

    text = text.lower()
    return text, links

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

# Supprimer entre [[]] s'il y a : dans les crochet, prends en compte les cas embrique
# Renvoie aussi tous les liens internes du text (entre les crochets sans :)
# text : le text où l'on veut supprimer des mots

def supprimerCrocher(text):
    links = ''
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
                links += (re.sub('(\[\[|\]\])', '', (entre.split('|')[0]).split('#')[0])).strip() + ';'
                result += entre
            doubleP = False
            entre = ''
        elif skip > 0:
            entre += mot + " "
            if ':' in mot:
                doubleP = True
        elif skip == 0:
            result += mot + " "
    return result, links


#text_processing
def text_processing(text, STOPWORDS, nlp):
    """
    Delete stop words
    Text lemmatization
    Text stemming

    Args:
        text (String): text to process

    Returns:
        String: text after eliminating stopwords, lemmatization and stemming
    """
    
    #nlp = fr_core_news_md.load()
    # ps = PorterStemmer()
    

    # Spell check
    #spell_checked = []
    #for word in text.split():
    #    spell_checked.append(spell.correction(word))


    # Deleting stopwords   
    #cleaned_test = " ".join([word for word in spell_checked if word not in STOPWORDS])
    cleaned_test = " ".join([word for word in text.split() if word not in STOPWORDS])

    # Lemmatization
    doc = nlp(cleaned_test)
    lemmatized = " ".join([token.lemma_ for token in doc])

    # Stemming
    # words = word_tokenize(lemmatized)
    # res = " ".join([ps.stem(w) for w in words])
    return lemmatized

#Fonction qui parcourt un fichier et applique text_processing
def process_file(input, output, STOPWORDS, nlp, id_link):
    outfile = open(output, 'w', encoding="utf-8")
    with open(input, encoding="utf-8", errors="ignore") as infile:
        n = 0
        for line in infile:
            n += 1
            print(f'\r {n/5}/65026   ', end = '\r')
            if (n % 5 == 0) or (n % 5 == 3):
                outfile.write(text_processing(line, STOPWORDS, nlp) + "\n")
            elif (n % 5 == 4):
                links = []
                for link in line.split(';'):
                    if (link in id_link):
                        links.append(str(id_link[link]))
                links = list(dict.fromkeys(links))
                outfile.write(" ".join(links) + "\n")
            else :
                outfile.write(line)
    print('\n')
   
   
#Coupe le fichier et creer un nouveau
#start inclus, end exclus

def cut_file(input, output , start, end):
    outfile = open(output, 'w', encoding="utf-8")
    with open(input, encoding="utf-8", errors="ignore") as infile:
        n = 0
        for line in infile:
            n += 1 
            print(f'\r {n/5}/{end}   ', end = '\r')
            if ((n - 1) / 5) + 1 >= start and ((n - 1) / 5) + 1 < end:
                outfile.write(line)
            elif ((n - 1) / 5) + 1 == end:
                return




#print(nombresPages('frwiki.xml'))
       

print("Préparation")

start_time = time.time()
STOPWORDS = set(stopwords.words('french'))
nlp = spacy.load('fr_core_news_md')
nlp.max_length = 2000000
tp = (time.time() - start_time)
print("--- %s seconds ---" % tp)

print("Limiter Corpus")

#limitCorpus('frwiki.xml','wikilimit.xml')

print("Nettoyage")

#id_link = nettoyer_file('wikilimit.xml', 'wikinettoye.xml', 200)
#cut_file("wikinettoye.xml", "wikinettoye1.xml", 1, 65026)
#cut_file("wikinettoye.xml", "wikinettoye2.xml", 65026, 130052)
#cut_file("wikinettoye.xml", "wikinettoye3.xml", 130052, 195078)
tc = (time.time() - start_time)
print("--- %s seconds ---" % (tc - tp))

print("Traitement du fichier")

print("1/3")
ts = (time.time() - start_time)
#process_file("wikinettoye1.xml", "wikiprocess1.xml", STOPWORDS, nlp, id_link)
te = (time.time() - start_time)
print("--- %s seconds ---" % (te - ts))

print("2/3")
ts = (time.time() - start_time)
#process_file("wikinettoye2.xml", "wikiprocess2.xml", STOPWORDS, nlp, id_link)
te = (time.time() - start_time)
print("--- %s seconds ---" % (te - ts))

print("3/3")
ts = (time.time() - start_time)
#process_file("wikinettoye3.xml", "wikiprocess3.xml", STOPWORDS, nlp, id_link)
te = (time.time() - start_time)
print("--- %s seconds ---" % (te - ts))

print("Finition")

ts = (time.time() - start_time)
#outfile = open("wikiprocess.xml", 'w', encoding="utf-8")
#with open("wikiprocess1.xml", encoding="utf-8", errors="ignore") as infile:
#    for line in infile:
#        outfile.write(line)
#with open("wikiprocess2.xml", encoding="utf-8", errors="ignore") as infile:
#    for line in infile:
#        outfile.write(line)
#with open("wikiprocess3.xml", encoding="utf-8", errors="ignore") as infile:
#    for line in infile:
#        outfile.write(line)
#cut_file("wikiprocess.xml", "wikiprocess1000.xml", 1, 1001)
#cut_file("wikiprocess.xml", "wikiprocess100.xml", 1, 101)
te = (time.time() - start_time)
print("--- %s seconds ---" % (te - ts))



