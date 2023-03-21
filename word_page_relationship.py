import math as m
from collections import Counter
import pickle
import time
from itertools import islice
from collections import defaultdict

def word_count(filename):
    """
    Count number of occurence of every words in the page corpus.
    Return the most common 20 000 words

    Args:
        filename (string): path to file

    Returns:
        dict<number:number>: dictionary associating words to their number of occurence
        number: number of pages
    """
    nb_page = 0
    counts = dict()
    step = 5
    with open(filename, 'r') as file:
        # for line in islice(file, 4, None, 5): # same efficiency
        for line_nb, line in enumerate(file, 1):
            if line_nb % 97583 == 0:
                print(f"{(line_nb / 975385) * 100} % (word count)")
            if line_nb % step == 0:
                nb_page += 1
                words = line.split()
                for word in words:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
    counts_sorted = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return dict(counts_sorted[:20000]), nb_page



def index(filename, keywords, nb_page):
    # def compute_tf_idf(word_page, page_norm, nb_page):
    #     for word, pages in word_page.items():
    #         idf = m.log10(nb_page / len(pages))
    #         for page, freq in pages.items():
    #             tf = 1 + m.log10(freq)
    #             tf_idf = tf * idf / page_norm[page]
    #             word_page[word][page] = tf_idf
    # def default_dict():
    #     """
    #     Without this function, the declaration
    #     word_page = defaultdict(lambda: defaultdict(int))
    #     in index()
    #     will provoke
    #     AttributeError: Can't pickle local object 'index.<locals>.<lambda>'
    #     at
    #     pickle.dump(word_page, f, pickle.HIGHEST_PROTOCOL)
    #     """
    #     return defaultdict(int)
    keywords = set(keywords)
    word_page = defaultdict(defaultdict(int)) #  dictionnaire qui représente la relation mot-page : {word : {page : tf(word,page)}}
    page_word = {page_id: set() for page_id in range(1, nb_page+1)} # use set() instead of list, much faster to check if element is inside
    page_norm = {} # dictionnaire qui associe à chaque page sa norme: {page : norm Nd}, used to store the pages' norm
    step = 5



    with open(filename, 'r') as file:
        for line_nb, line in enumerate(file, 1):
            if line_nb % 9758 == 0:
                print(f"{(line_nb / 975385) * 100} % (index)")
            if line_nb % step == 0:
                page_id = line_nb//step
                words = line.split()

                for word in words: # Compute number of occurence and update word page relation
                    if word in keywords:
                        word_page[word][page_id] += 1
                        page_word[page_id].add(word)

                # Compute TF as defined in TP1, Exercice 8.1
                for word_key in word_page.keys(): # for each word
                    for page_key in word_page[word_key].keys(): # for each page containing said word
                        word_page[word_key][page_key] = 1 + m.log10(word_page[word_key][page_key]) 

        for page_id, words in page_word.items():
            norm = sum((1 + m.log10(word_page[word][page_id]))**2 for word in words)
            page_norm[page_id] = m.sqrt(norm)

        for word, pages in word_page.items():
            idf = m.log10(nb_page / len(pages))
            for page, freq in pages.items():
                tf = 1 + m.log10(freq)
                tf_idf = tf * idf / page_norm[page]
                word_page[word][page] = tf_idf

    with open('data/data.pickle', 'wb') as f:
        pickle.dump(word_page, f, pickle.HIGHEST_PROTOCOL)

    return word_page




# COMPUTE WORD PAGE DICTIONARY
t1 = time.time()
word_occurence, nb_page = word_count("data/pages/wikiprocess1000.txt")
keywords = list(word_occurence.keys())
word_page = index("data/pages/wikiprocess1000.txt",keywords, nb_page)
print(word_page)
print(time.time() - t1)

# {'gt': 3649138, 'lt': 3620439, 'quot': 3052610, 'avoir': 1456511, 'ref': 1094109, 'football': 1013069,
# 'name': 967920, 'championnat': 931275, 'ce': 884718, 'plus': 828003, 'équipe': 815204, 'faire': 698181,
# 'premier': 692309, 'france': 648700, 'club': 635931, 'pouvoir': 632903, 'saison': 571626, 'amp': 555965,
# 'small': 554353, 'deux': 519903}
# 68.35061240196228

# LOAD SAVED WORD PAGE DICTIONARY

# with open('data/data.pickle', 'rb') as f:
#     test = pickle.load(f)
# print(test)