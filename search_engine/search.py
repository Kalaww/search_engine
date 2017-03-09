import pandas

import search_engine.util as util

def preprocess_request(request, word_to_id):
    """
    Transform request of words in corresponding words id set
    :param request:
    :param word_to_id:
    :return:
    """
    request = util.lower_and_no_accent(request)
    words_id = [word_to_id[w] for w in request.split() if w in word_to_id]
    return sorted(set(words_id))

def load_words_appearance(filename):
    fd = open(filename, 'r')
    first_line = True
    data = {}
    for line in fd.readlines():
        if first_line:
            first_line = False
            continue
        word_id, frequencies = line[:-1].split(',')
        frequencies = frequencies.split()
        freq = []
        for i in frequencies:
            a,b = i.split(':')
            freq.append((int(a),float(b)))
        data[int(word_id)] = freq
    fd.close()
    return data

def load_page_score(filename):
    fd = open(filename, 'r')
    data = {}
    i = 0
    for line in fd.readlines():
        data[float(line[:-1])] = i
        i += 1
    fd.close()
    page_score = [data[score] for score in reversed(sorted(data))]
    return page_score

def load_id_to_page(filename):
    dataframe = pandas.read_csv(filename, sep='@')
    id_to_page = {}
    for i in range(len(dataframe)):
        id_to_page[dataframe['id'][i]] = dataframe['page'][i]
    return id_to_page

def get_results(request, page_score, words_appearance):
    request_pages = []
    request_titles = []
    for word_id in request:
        request_titles.append(set(sorted(set([page for page,freq in words_appearance[word_id] if freq > 1.0]))))
        request_pages.append(set(sorted(set([page for page,freq in words_appearance[word_id]]))))
    request_titles = set.intersection(*request_titles)
    request_pages = set.intersection(*request_pages)

    result_titles = [page_id for page_id in page_score if page_id in request_titles]
    result_pages = [page_id for page_id in page_score if page_id in request_pages]
    return result_titles, result_pages

def search(request, dictionary_filename, words_appearance_filename, page_score_filename, id_to_page_filename):
    word_to_id = util.load_dictionary(dictionary_filename, with_word_to_id=True)
    words_appearance = load_words_appearance(words_appearance_filename)
    page_score = load_page_score(page_score_filename)
    id_to_page = load_id_to_page(id_to_page_filename)

    request_id = preprocess_request(request, word_to_id)
    results_titles, results_pages = get_results(request_id, page_score, words_appearance)

    fd = open('result.txt', 'w')
    fd.write('## RESULTS TITLE\n')
    for page_id in results_titles:
        fd.write(id_to_page[page_id]+'\n')
    fd.write('\n## RESULTS PAGE\n')
    for page_id in results_pages:
        fd.write(id_to_page[page_id]+'\n')
    fd.close()

