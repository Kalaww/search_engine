# coding: utf-8

from __future__ import print_function, division
import search_engine.util as util
import os
import re


def extract_links(page_id, page_content, title_to_id):
    """
    Search for links in page content
    :param page_id:
    :param page_content:
    :param title_to_id:
    :return:
    """
    re_link = '\[\[(.*?)\]\]'
    match = re.findall(re_link, page_content)
    links = []
    if match:
        for m in match:
            for m1 in m.split('|'):
                if ':' in m1:
                    continue
                m1 = util.normalize_text(util.lower_and_no_accent(m1))
                if m1 in title_to_id:
                    links = links + title_to_id[m1]
    return sorted(set(links) - set([page_id]))


def extract_words_id(text, word_to_id):
    """
    Convert a text to an array of word ids
    :param text:
    :param word_to_id:
    :return:
    """
    text = util.lower_and_no_accent(text)
    text = util.normalize_text(text)
    return [word_to_id[w] for w in text.split(' ') if w in word_to_id]


def append_to_words_appearance(words_appearance, page_id, title, words_id, word_to_id, pages_per_word):
    """
    Append words frequences to the words_appearance map
    The frequency of a word in the words_id is between 0 and 1
    The words in the title add the value 1 to the frequency of the corresponding word
    :param words_appearance:
    :param page_id:
    :param title:
    :param words_id:
    :param word_to_id:
    :param pages_per_word:
    :return:
    """
    title_words_id = set([word_to_id[w] for w in title.split(' ') if w in word_to_id])
    freq_unique = 1.0 / float(len(words_id))
    occ = dict()
    for word_id in words_id:
        if word_id in occ:
            occ[word_id] += freq_unique
        else:
            occ[word_id] = freq_unique
    for word_id in title_words_id:
        if word_id in occ:
            occ[word_id] += 1.0
        else:
            occ[word_id] = 1.0
    for k, v in occ.items():
        if k in words_appearance:
            words_appearance[k].append((v, page_id))
            if len(words_appearance[k]) > pages_per_word:
                words_appearance[k] = (sorted(words_appearance[k]))[1:]
        else:
            words_appearance[k] = [(v, page_id)]


def fetch_titles(wiki_filename, progressBar, print_interval):
    pageID_to_title = {}
    title_to_pageID = {}

    re_title = '.*<title>(.+)</title>.*'
    re_id = '.*<id>(\d+)</id>.*'

    line_count = 0
    my_id = 1

    title = None
    title_raw = None

    print('\nSearch for page titles')
    progressBar.reset_time()
    with open(wiki_filename, 'r') as fd_wiki:
        for line in fd_wiki:
            line = line[:-1]
            line = line.strip()
            if '<title' in line:
                match = re.match(re_title, line)
                if match is None or ':' in match.group(1):
                    continue
                title_raw = match.group(1)
                title = util.normalize_text(util.lower_and_no_accent(title_raw))
            elif '<id' in line and not title is None:
                match = re.match(re_id, line)
                if match is None:
                    continue
                pageID = int(match.group(1))
                pageID_to_title[pageID] = (my_id, title, title_raw)
                if not title in title_to_pageID:
                    title_to_pageID[title] = []
                title_to_pageID[title].append(my_id)
                title = None
                title_raw = None
                my_id += 1

            if line_count % print_interval == 0:
                progressBar.print_progress(line_count)
            line_count += 1

    print(' DONE')
    print(util.pretty_number(len(title_to_pageID)), 'titles found\n')

    return pageID_to_title, title_to_pageID


def fetch_pages(wiki_filename, page_links_filename, pageID_to_title, title_to_pageID, word_to_id, pages_per_word, progressBar, print_interval):
    in_page = False
    in_text = False

    words = None
    pageID = None

    re_id = '.*<id>(\d+)</id>.*'
    re_text_start = '^.*<text.*>(.+)$'
    re_text_end = '^(.*)</text>'
    re_text_start_end = '^.*<text.*>(.+)</text'

    words_appearance = dict()

    fd_links = open(os.path.join(page_links_filename), 'w')

    line_count = 0

    print('\nCollecting text of each page')
    progressBar.reset_time()
    with open(wiki_filename, 'r') as fd_wiki_dump:
        for line in fd_wiki_dump:
            line = line[:-1]
            line = line.strip()
            if in_page:
                if in_text:
                    if '</text' in line:
                        match = re.match(re_text_end, line)
                        if match is None:
                            continue
                        words += ' ' + match.group(1)
                        in_text = False
                    else:
                        words += ' ' + line
                else:
                    if '</page' in line:
                        if words and not pageID is None and pageID > -1:
                            myID, title = pageID_to_title[pageID]
                            links = extract_links(myID, words, title_to_pageID)
                            for link in links:
                                fd_links.write('{}\t{}\n'.format(myID, link))

                            words_id = extract_words_id(words, word_to_id)
                            if len(words_id) > 0:
                                append_to_words_appearance(
                                    words_appearance,
                                    myID,
                                    title,
                                    words_id,
                                    word_to_id,
                                    pages_per_word
                                )
                        words = None
                        pageID = None
                        in_page = False
                    elif '<id' in line and pageID is None:
                        match = re.match(re_id, line)
                        if match is None:
                            continue
                        pageID = int(match.group(1))
                        if not pageID in pageID_to_title:
                            pageID = -1
                    elif '<text' in line and not pageID is None:
                        if '</text' in line:
                            match = re.match(re_text_start_end, line)
                            if match is None:
                                continue
                            words = match.group(1)
                        else:
                            match = re.match(re_text_start, line)
                            if match is None:
                                continue
                            words = match.group(1)
                            in_text = True
            else:
                if '<page' in line:
                    in_page = True
            if line_count % print_interval == 0:
                progressBar.print_progress(line_count)
            line_count += 1

    fd_links.close()
    print('  DONE\n')
    return words_appearance


def run(wiki_filename, output_dir, dictionary_filename, print_interval=10000, pages_per_word=10, lines_count=None):
    if wiki_filename is None:
        return
    if output_dir is None:
        return

    PAGEID_TO_TITLE_FILENAME = os.path.join(output_dir, 'pageID_to_title.txt')
    PAGE_LINKS_FILENAME = os.path.join(output_dir, 'page_links.txt')
    WORDS_APPEARANCE_FILENAME = os.path.join(output_dir, 'words_appearance.csv')

    WIKI_N_LINES = lines_count
    if WIKI_N_LINES is None :
        print('Counting lines in wiki file')
        WIKI_N_LINES = util.count_lines_in_file(wiki_filename)
        print('Result:', util.pretty_number(WIKI_N_LINES))

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    print('\nLoading dictionnary of words ...')
    word_to_id, id_to_word = util.load_dictionary(dictionary_filename, with_word_to_id=True, with_id_to_word=True)
    print('Dictionnary loaded')

    progressBar = util.ProgressBar(WIKI_N_LINES)

    pageID_to_title, title_to_pageID = fetch_titles(wiki_filename, progressBar, print_interval)

    print('Saving [pageID -> title] into file', PAGEID_TO_TITLE_FILENAME)
    util.save_pageID_to_title(PAGEID_TO_TITLE_FILENAME, sorted(pageID_to_title.values()))

    words_appearance = fetch_pages(
        wiki_filename,
        PAGE_LINKS_FILENAME,
        pageID_to_title,
        title_to_pageID,
        word_to_id,
        pages_per_word,
        progressBar,
        print_interval
    )

    print('Saving [words appearance] into file', WORDS_APPEARANCE_FILENAME)
    util.save_words_appearance(WORDS_APPEARANCE_FILENAME, words_appearance)

    print('\n== OUTPUT FILES ==')
    print('{} : contains id -> page title relation'.format(PAGEID_TO_TITLE_FILENAME))
    print('{} : contains page id -> links page id'.format(PAGE_LINKS_FILENAME))
    print('{} : contains word id -> list(page id)'.format(WORDS_APPEARANCE_FILENAME))