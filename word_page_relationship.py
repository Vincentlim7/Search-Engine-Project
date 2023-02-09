import math as m
from collections import Counter
import pickle
import _pickle as cPickle

def word_count(fname):
    counts = dict()
    step = 3
    with open(fname) as handle:
        for lineno, line in enumerate(handle):
            if lineno % step == 0:
                words = line.split()
                for word in words:
                    if word in counts:
                        counts[word] += 1
                    else:
                        counts[word] = 1
    counts_sorted = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
    return counts_sorted

def index(filename, lst):
    lst = set(lst)
    word_page = {} #  dictionnaire qui représente la relation mot-page : {word : {page : tf(word,page)}}
    page_word =  {} # dictionnaire qui associe à chaque page, l'ensemble des mots y apparaissant et appartenant à lst: {page : [word]}
    page_norm = {} # dictionnaire qui associe à chaque page sa norme: {page : norm Nd}
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

        # print(word_page)
        # Compute vector norm as defined in TP1, Exercice 8.2
        # print(page_word)
        # print("----------")
        for key, val in page_word.items():
            res = 0
            for word in val:
                # print(word, ", ", key, ", ",word_page[word])
                res += word_page[word][key]**2
            if res < 0:
                print(f"RES NEGATIF : {res}")
            page_norm[key] = m.sqrt(res)
        
        for word, val in word_page.items():
            for page in val.keys():
                word_page[word][page] /= page_norm[page]

    with open('data/data.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(word_page, f, pickle.HIGHEST_PROTOCOL)
    # return word_page, page_word, page_norm
    return word_page




# COMPUTE WORD PAGE DICTIONARY

x = word_count("data/test.xml")
y = list(x.keys())
# word_page, page_word, page_norm = index("data/test.xml",y)
word_page = index("data/test.xml",y)
print(word_page)



# LOAD SAVED WORD PAGE DICTIONARY

# with open('data/data.pickle', 'rb') as f:
#     test = pickle.load(f)
# print(test)