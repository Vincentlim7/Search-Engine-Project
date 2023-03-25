import math as m
from collections import Counter
import pickle
import time
from itertools import islice
from collections import defaultdict, Counter, OrderedDict

class Word_Page_CLI():
    def __init__(self, filename):
        """
        Create CLI matrix from file.

        Args:
            param (string or List<List<Float>>): either path to file or matrix to convert to CLI
            fromFile (boolean): True if creating matrix from file, else from matrix
        """
        self.nb_pages = 195077
        self.tenth_pages = self.nb_pages // 10

        self.word_id = OrderedDict() # associate a word to its column for the CLI matrix
                                     # OrderedDict so we can iterate on self.word_id.val() when computing IDF
        self.C = []
        self.L = [0] # initialized with 0 since the first row of the matrix start at index 0 of self.C
        self.I = []

        page_norm = {} # dictionnaire qui associe Ã  chaque page sa norme: {page : norm Nd}, used to store the pages' norm
        word_nb_page = [0 for i in range(len(keywords))] # nb of page containing word (used to compute IDF)
        page_id = 0
        word_id_counter = 0
        processed_lines = 0

        keywords = self.word_count(filename)
        with open(filename, 'r') as file:
            for line in islice(file, 4, None, 5):
                page_id += 1 
                words = line.split()
                C_bis = [] # coeff list for current line (will be added to self.C)
                # I_bis = [] # column number list for current line (will be added to self.I)
                C_bis_index = dict() # list of words already seen in current page

                for word in words: # Compute #occ(word, page) and add to C_bis
                    if word in keywords:
                        if word not in self.word_id: # new word, map it to an id
                            self.word_id[word] = word_id_counter
                            word_id_counter += 1

                        if word not in C_bis_index:
                            C_bis_index[word] = len(C_bis) # give its index in C_bis
                            C_bis.append(1) 
                            self.I.append(self.word_id[word])
                            word_nb_page[self.word_id[word]] += 1 # increse nb of page containing word
                        else:
                            C_bis[C_bis_index[word]] += 1
        
                C_bis = [1 + m.log10(occ) for occ in C_bis] # trasnform #occ(word, page) to TF(word, page) as defined in 8.1
                self.C.extend(C_bis) # at this point, self.C contains TF(word, page)
                # self.I.extend(I_bis)
                self.L.append(len(self.C)) # an entire row of the matrix has been processed, so the next value is in a new row

                processed_lines += 1
                if processed_lines % self.tenth_pages == 0:
                    print(f"word_page_CLI() has processed {(processed_lines/self.nb_pages)*100:.2f}% of the file")


            # Compute TF as defined in TP1, Exercice 8.1
            # for i in range(len(self.C)): # for each word
            #     self.C[i] = 1 + m.log10(self.C[i]) # Compute TF(word,page) as defined in 8.1
                
            # Compute norm vector as defined in 8.2
            print("Computing norms")
            processed = 0
            nb_iteration = len(self.L)
            tenth_iteration = nb_iteration // 10
            for i in range(1, len(self.L)):
                norm = sum(self.C[j]**2 for j in range(self.L[i-1], self.L[i]))
                page_norm[i-1] = m.sqrt(norm)
                processed += 1
                if processed % tenth_iteration == 0:
                    print(f"Computing norms has processed {(processed/nb_iteration)*100:.2f}% of its iteration")

            # Compute IDF
            print("Computing IDF")
            processed = 0
            nb_iteration = len(keywords)
            tenth_iteration = nb_iteration // 10
            idf = []
            for i in self.word_id.values():
                idf.append(m.log10(self.nb_pages / word_nb_page[i]))  # idf will have the same order as self.word_id since its a OrderedDict 
                processed += 1
                if processed % tenth_iteration == 0:
                        print(f"Computing IDF has processed {(processed/nb_iteration)*100:.2f}% of its iteration")

            # Compute TF-IDF as defined in 8.4
            print("Computing TF-IDF")
            processed = 0
            nb_iteration = len(self.C)
            tenth_iteration = nb_iteration // 10
            page_id = 0
            for i in range(len(self.C)): # i is the index of the examined cell in C
                if i >= self.L[page_id+1]: # i is higher 
                    page_id += 1
                self.C[i] = self.C[i] * idf[self.I[i]] / page_norm[page_id]
                processed += 1
                if processed % tenth_iteration == 0:
                        print(f"Computing TF-IDF has processed {(processed/nb_iteration)*100:.2f}% of its iteration")

        with open('data/data.pickle', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def word_count(self, filename):
        """
        Count the number of occurence of every words in the page corpus.
        Return the most common 20 000 words

        Args:
            filename (string): path to file

        Returns:
            dict<number:number>: dictionary associating words to their number of occurence
            number: number of pages
        """
        counts = Counter()
        processed_pages = 0
        with open(filename, 'r') as file:
            for line in islice(file, 4, None, 5):
                words = line.split()
                counts.update(words) # update the counters for all word in words
                processed_pages += 1
                if processed_pages % self.tenth_pages == 0:
                    print(f"word_count() has processed {(processed_pages/self.nb_pages)*100:.2f}% of the file")
                
        return set([item[0] for item in counts.most_common(20000)]) # item is a tuple (word, nb_occurence), convert to set because more efficient to test existence

word_page_CLI = Word_Page_CLI("./data/pages/wikiprocess.txt")

# with open('data/data.pickle', 'rb') as f:
#     word_page_CLI = pickle.load(f)