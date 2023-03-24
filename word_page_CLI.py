import math as m
from collections import Counter
import pickle
import time
from itertools import islice
from collections import defaultdict, Counter

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
        self.step = 5

        self.word_id = dict()

        word_page = defaultdict(default_dict) #  dictionnaire qui représente la relation mot-page : {word : {page : tf(word,page)}}
        page_word = {page_id: set() for page_id in range(1, nb_page+1)} # use set() instead of list, much faster to check if element is inside
        page_norm = {} # dictionnaire qui associe à chaque page sa norme: {page : norm Nd}, used to store the pages' norm
        step = 5
        page_id = 0
        processed_lines = 0

        with open(filename, 'r') as file:
            for line in islice(file, 4, None, step):
                page_id += 1 
                words = line.split()

                for word in words: # Compute number of occurence and update word page relation
                    if word in keywords:
                        word_page[word][page_id] += 1 # at this point, word_page[word][page_id] contains #occ(word, page)
                        page_word[page_id].add(word)

                # Compute TF as defined in TP1, Exercice 8.1
                for word_key in word_page.keys(): # for each word
                    for page_key in word_page[word_key].keys(): # for each page containing said word
                        word_page[word_key][page_key] = 1 + m.log10(word_page[word_key][page_key]) # Compute TF(word,page) as defined in 8.1
                
                processed_lines += step
                if processed_lines % tenth_lines == 0:
                    print(f"word_count() has processed {(processed_lines/total_lines)*100:.2f}% of the file")

            # Compute norm vector as defined in 8.2
            print("Computing norms")
            for page_id, words in page_word.items():
                norm = sum(word_page[word][page_id]**2 for word in words)
                page_norm[page_id] = m.sqrt(norm)

            # Compute TF-IDF as defined in 8.4
            print("Computing TF-IDF")
            for word, pages in word_page.items():
                idf = m.log10(nb_page / len(pages))
                for page, freq in pages.items():
                    tf = 1 + m.log10(freq)
                    tf_idf = tf * idf / page_norm[page]
                    word_page[word][page] = tf_idf

        with open('data/data.pickle', 'wb') as f:
            pickle.dump(word_page, f, pickle.HIGHEST_PROTOCOL)

        return word_page

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
            for line in islice(file, 4, None, self.step):
                words = line.split()
                counts.update(words) # update the counters for all word in words
                processed_pages += 1
                if processed_pages % self.tenth_pages == 0:
                    print(f"word_count() has processed {(processed_pages/self.nb_pages)*100:.2f}% of the file")
                
        self.keywords = set([item[0] for item in counts.most_common(20000)]) # item is a tuple (word, nb_occurence), convert to set because more efficient to test existence 