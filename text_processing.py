import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from spellchecker import SpellChecker

import spacy
import fr_core_news_md


#nltk.download('stopwords')

import time
start_time = time.time()

# Downloading nltk ressources (only need to be done once)
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')


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
def process_file(input, output, STOPWORDS, nlp):
    outfile = open(output, 'w', encoding="utf-8")
    with open(input, encoding="utf-8", errors="ignore") as infile:
        n = 0
        for line in infile:
            n += 1
            print(f'\r {n/4}/65026   ', end = '\r')
            if n % 4 == 0:
                outfile.write(text_processing(line, STOPWORDS, nlp) + "\n")
            else :
                outfile.write(line)
    print('\n')
   
#Coupe le fichier et creer un nouveau
#start inclus, end exclus. Ils represente l'id de la page wiki
def cut_file(input, output , start, end):
    outfile = open(output, 'w', encoding="utf-8")
    with open(input, encoding="utf-8", errors="ignore") as infile:
        n = 0
        for line in infile:
            n += 1 
            print(f'\r {n/4}/{end}   ', end = '\r')
            if ((n - 1) / 4) + 1 >= start and ((n - 1) / 4) + 1 < end:
                outfile.write(line)
            elif ((n - 1) / 4) + 1 == end:
                return


#Les nom des fichiers
input = 'wikinettoye1.xml'
output = 'wikiprocess1.xml'

STOPWORDS = set(stopwords.words('french'))
nlp = spacy.load('fr_core_news_md')
#spell = SpellChecker(language='fr')

tp = (time.time() - start_time)

print("--- Préparation: %s seconds ---" % tp)


#test = "Dresser la liste des mots sur lesquels pourront porter les requêtes de l utilisateur aimerions étaient sommes matinnn auront était est suis es l l le la notre buvions mangerai animaux"
#print(test)
#print(text_processing(test, STOPWORDS, nlp))

print("Couper le fichier")
#cut_file("wikinettoye.xml", "wikinettoye3.xml", 130052, 195078)
tc = (time.time() - start_time)
print("--- %s seconds ---" % (tc - tp))

print("Traitement du fichier")
process_file(input, output, STOPWORDS, nlp)
tf = (time.time() - start_time)
print("--- %s seconds ---" % (tf - tc))
