from word_page_CLI import Word_Page_CLI
from link_CLI import Link_CLI
import pickle
if __name__=="__main__":

    print("LOADING title_map")
    with open('data/title_map.pickle', 'rb') as f:
        title_map = pickle.load(f)


    ## COMPUTE NEW WORD_PAGE_CLI AND LINK_CLI

    # word_page_CLI = Word_Page_CLI("./data/pages/wikiprocess.txt")
    # print(f"len of C : {len(word_page_CLI.C)}") # 6 159 228 -> 6 148 125 (nb after deleting links to page_id > max_id(pages))
    # print(f"len of L : {len(word_page_CLI.L)}") # 195 078 -> 195 078
    # print(f"len of I : {len(word_page_CLI.I)}") # 6 159 228 -> 6 148 125

    # link_CLI = Link_CLI("data/pages/wikiprocessnew.txt")
    # print(f"len of C : {len(link_CLI.C)}") # 6 159 228 -> 6 148 125 (nb after deleting links to page_id > max_id(pages))
    # print(f"len of L : {len(link_CLI.L)}") # 195 078 -> 195 078
    # print(f"len of I : {len(link_CLI.I)}") # 6 159 228 -> 6 148 125
    # print(f"sum of pagerank : {sum(link_CLI.v)}")


    ## LOAD EXISTING WORD_PAGE_CLI, LINK_CLI, PAGERANK

    print("LOADING word_page_CLI")
    with open('data/word_page_CLI.pickle', 'rb') as f:
        word_page_CLI = pickle.load(f)
        print(len(word_page_CLI.C))
        print(len(word_page_CLI.L))
        print(len(word_page_CLI.I))


    # print("LOADING link_CLI")
    # with open('data/link_CLI.pickle', 'rb') as f:
    #     link_CLI = pickle.load(f)
    #     print(f"len of C : {len(link_CLI.C)}")
    #     print(f"len of L : {len(link_CLI.L)}")
    #     print(f"len of I : {len(link_CLI.I)}")
    #     print(f"sum of pagerank : {sum(link_CLI.v)}") # Change desired epsilon and k in the function

    print("LOADING pagerank")
    with open('data/pagerank_e0.14_i200.pickle', 'rb') as f:
        pagerank = pickle.load(f)
        print(f"len of pagerank : {len(pagerank)}") # Should be same as len(L) of CLI matrix
        print(f"sum of pagerank : {sum(pagerank)}")

    ## TESTING FUNCTIONS

    # Test simple_query
    # 

    # print(link_CLI.pagerank_compute_best_iterations()) # episolon = 1/7 --> 7
    # print(link_CLI.pagerank_compute_best_params())
    # link_CLI.pagerank(200)

    query_res = word_page_CLI.simple_query(["autriche", "forme", "long", "république", "autrich", "état", "fédéral", "europe", "central", "pays", "sans"], pagerank)
    for page_id, score in query_res:
        print(f"{title_map[page_id]} : {score}")