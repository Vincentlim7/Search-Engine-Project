import math as m
from collections import Counter
import pickle
import _pickle as cPickle

def word_count(fname):
    nb_page = 0
    counts = dict()
    step = 3
    with open(fname) as handle:
        for lineno, line in enumerate(handle):
            if lineno % step == 0:
                nb_page += 1
                words = line.split()
                for word in words:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
    counts_sorted = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    return counts_sorted, nb_page

def index(filename, lst, nb_page):
    lst = set(lst)
    # idf = {} # dictionnaire qui associe un mot à son idf : {word : idf(word)}
    word_page = {} #  dictionnaire qui représente la relation mot-page : {word : {page : tf(word,page)}}
    page_word =  {} # dictionnaire qui associe à chaque page, l'ensemble des mots y apparaissant et appartenant à lst: {page : [word]}, used to compute norm (q8.2)
    page_norm = {} # dictionnaire qui associe à chaque page sa norme: {page : norm Nd}, used to store the pages' norm
    with open(filename, 'r') as fobj:
        for lineno, line in enumerate(fobj, 1):
            if lineno % 4 == 0:
                page_id = lineno//4
                words = line.split()

                for word in words: # Compute number of occurence and update word page relation
                    if word in lst:
                        if word not in word_page:
                            word_page[word] = {page_id : 1}
                        else:
                            if page_id not in word_page[word]:
                                word_page[word][page_id] = 1
                            else:
                                word_page[word][page_id] += 1
                            
                        if page_id not in page_word:
                            page_word[page_id] = []
                        if word not in page_word[page_id]:
                            page_word[page_id].append(word)

                # Compute TF as defined in TP1, Exercice 8.1
                for word_key in word_page.keys(): # for each word
                    for page_key in word_page[word_key].keys(): # for each page containing said word
                        word_page[word_key][page_key] = 1 + m.log10(word_page[word_key][page_key]) 

        # Compute vector norm as defined in TP1, Exercice 8.2
        for key, val in page_word.items():
            res = 0
            for word in val:
                res += word_page[word][key]**2
            page_norm[key] = m.sqrt(res)
        
        for word, val in word_page.items():
            for page in val.keys():
                word_page[word][page] /= page_norm[page]
        
        # Compute IDF as defined in TP1, Exercice 3
        for word, val in word_page.items():
            idf = nb_page / len(val)
            for page in val.keys():
                word_page[word][page] *= idf
                # if word_page[word][page] < 10: # threshold to modify
                #     del word_page[word][key]



    with open('data/data.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(word_page, f, pickle.HIGHEST_PROTOCOL)
    # return word_page, page_word, page_norm
    return word_page




# COMPUTE WORD PAGE DICTIONARY

x, nb_page = word_count("data/wikiprocess.xml")
y = list(x.keys())
# word_page, page_word, page_norm = index("data/test.xml",y)
word_page = index("data/wikiprocess.xml",y, nb_page)
print(word_page)



# LOAD SAVED WORD PAGE DICTIONARY

# with open('data/data.pickle', 'rb') as f:
#     test = pickle.load(f)
# print(test)