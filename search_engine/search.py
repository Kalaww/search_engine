import search_engine.util as util

WIKI_URL = 'https://fr.wikipedia.org/wiki/{page}'

def preprocess_request(request, word_to_id):
    """
    Transform request of words in corresponding words id set
    :param request:
    :param word_to_id:
    :return:
    """
    request = util.lower_and_no_accent(request)
    words_id = [word_to_id[w] for w in request.split() if w in word_to_id]
    return sorted(set(words_id)), '-'.join(request.split())


def get_results(request, page_score, words_appearance):
    request_pages = []
    for word_id in request:
        if word_id in words_appearance:
            request_pages.append(set(words_appearance[word_id]))
    if len(request_pages) is 0:
        return None
    request_pages = set.intersection(*request_pages)
    result_pages = [page_id for page_id in page_score if page_id in request_pages]
    return [(i, p) for i,p in enumerate(result_pages)]


def get_page_title(results_pages, id_to_page_filename):
    out = []
    done = len(results_pages)
    fd = open(id_to_page_filename, 'r')
    for line in fd.readlines():
        id, page = line[:-1].split(' ')
        page = page.replace('_', ' ')
        id = int(id)
        for pos, page_id in results_pages:
            if page_id == id:
                out.append((pos, page))
                results_pages.remove((pos, page_id))
                done -= 1
                if done <= 0:
                    break
                continue
    fd.close()
    tmp, ret = zip(*sorted(out))
    return ret


def search(dictionary_filename, words_appearance_filename, page_score_filename, pageID_to_title_filename, verbose=False):
    if verbose:
        print('Loading dictionary')
    word_to_id = util.load_dictionary(dictionary_filename, with_word_to_id=True)

    if verbose:
        print('Loading words appearance ...')
    words_appearance = util.load_words_appearance(words_appearance_filename)

    if verbose:
        print('Loading page score ...')
    page_score = util.load_page_score(page_score_filename)

    while True:
        print('SEARCH (\q to quit)')
        request = input('-> ')
        if request == '\q':
            return
        request_id, result_filename = preprocess_request(request, word_to_id)
        if len(request_id) == 0:
            print('Request contains no words in the dictionary\n')
            continue

        results_pages = get_results(request_id, page_score, words_appearance)
        if results_pages is None:
            print('No result found\n')
            continue
        titles = get_page_title(results_pages, pageID_to_title_filename)

        result_filename += '.txt'
        fd = open(result_filename, 'w')
        i = 1
        print('\nRESULTS')
        for title in titles:
            l = '{}: {} {}'.format(i, title, WIKI_URL.format(page=title))
            print(l)
            fd.write(l+'\n')
            i += 1
        fd.close()
        print("\nResults saved in '{}'\n".format(result_filename))

