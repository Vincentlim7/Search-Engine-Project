import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from spellchecker import SpellChecker

# Downloading nltk ressources (only need to be done once)
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

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
    STOPWORDS = set(stopwords.words('french'))
    nlp = spacy.load('fr_core_news_md')
    # ps = PorterStemmer()
    spell = SpellChecker(language='fr')

    # Spell check
    spell_checked = []
    for word in text.split():
        spell_checked.append(spell.correction(word))


    # Deleting stopwords   
    cleaned_test = " ".join([word for word in spell_checked if word not in STOPWORDS])

    # Lemmatization
    doc = nlp(cleaned_test)
    lemmatized = " ".join([token.lemma_ for token in doc])

    # Stemming
    # words = word_tokenize(lemmatized)
    # res = " ".join([ps.stem(w) for w in words])
    return lemmatized

test = "Dresser la liste des mots sur lesquels pourront porter les requêtes de l utilisateur aimerions étaient sommes matinnn auront était est suis es l l le la notre buvions mangerai animaux"
print(test)
print(text_processing(test))