import nltk
from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from spellchecker import SpellChecker
import spacy
import fr_core_news_md
import time

# Downloading nltk ressources (only need to be done once)
# nltk.download('stopwords')
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
start_time = time.time()
STOPWORDS = set(stopwords.words('french'))
nlp = spacy.load('fr_core_news_md')
spell = SpellChecker(language='fr')
# ps = PorterStemmer()

print("--- %s seconds ---" % (time.time() - start_time))

def text_processing(text):
    """
    Delete stop words
    Text lemmatization
    Text stemming

    Args:
        text (String): text to process

    Returns:
        String: text after eliminating stopwords, lemmatization and stemming
    """
    
    # Spell check
    # spell_checked = []
    # for word in text.split():
    #    spell_checked.append(spell.correction(word))


    # Deleting stopwords 
    # cleaned_test = " ".join([word for word in spell_checked if word not in STOPWORDS])
    cleaned_test = " ".join([word for word in text.split() if word not in STOPWORDS])
    
    # Lemmatization
    doc = nlp(cleaned_test)
    lemmatized = " ".join([token.lemma_ for token in doc])

    # Stemming
    # words = word_tokenize(lemmatized)
    # res = " ".join([ps.stem(w) for w in words])

    return lemmatized


input = 'data/test.xml'
output = 'data/test_output.xml'

outfile = open(output, 'w', encoding="utf-8")
with open(input, encoding="utf-8", errors="ignore") as infile:
    n = 0
    for line in infile:
        n += 1
        print(f'\r {n/4}/195077   ', end = '\r')
        if n % 4 == 0:
            outfile.write(text_processing(line) + "\n")
        else :
            outfile.write(line)
        
print("--- %s seconds ---" % (time.time() - start_time))