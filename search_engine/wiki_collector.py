# coding: utf-8

from __future__ import print_function, division
import search_engine.util as util
import os
import re


def extract_links(page_id, page_content, page_to_id):
    """
    Search for links in page content
    :param page_id:
    :param page_content:
    :param page_to_id:
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
                m1 = util.normalize_text(m1)
                if m1 in page_to_id:
                    links = links + page_to_id[m1]
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


def run(wiki_dump_filename, output_dir, dictionary_filename, print_interval=10000, pages_per_word=10, lines_count=None):
    if wiki_dump_filename is None:
        return
    if output_dir is None:
        return

    ID_TO_PAGE_FILENAME = os.path.join(output_dir, 'id_to_page.csv')
    PAGE_LINKS_FILENAME = os.path.join(output_dir, 'page_links.txt')
    WORDS_APPEARANCE_FILENAME = os.path.join(output_dir, 'words_appearance.csv')

    WIKI_N_LINES = lines_count
    if WIKI_N_LINES is None :
        print('Counting lines in wiki file')
        WIKI_N_LINES = util.count_lines_in_file(wiki_dump_filename)
        print('Result:', util.pretty_number(WIKI_N_LINES))

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


    print('\nLoading dictionnary of words ...')
    word_to_id, id_to_word = util.load_dictionary(dictionary_filename, with_word_to_id=True, with_id_to_word=True)
    print('Dictionnary loaded')


    page_to_id = {}  # page title => [ids]
    id_to_page = {}  # id => page title

    progressBar = util.ProgressBar(WIKI_N_LINES)
    re_title = '.*<title>(.+)</title>.*'
    line_count = 0
    page_id = 1

    print('\nSearch for page titles in file')
    with open(wiki_dump_filename, 'r') as fd_wiki_dump:
        for line in fd_wiki_dump:
            line = line[:-1]
            line = line.strip()
            if '<title' in line:
                line = util.lower_and_no_accent(line)
                match = re.match(re_title, line)
                if match is None or ':' in match.group(1):
                    continue
                current_title = match.group(1)
                current_title = util.normalize_text(current_title)
                if current_title in page_to_id:
                    page_to_id[current_title].append(page_id)
                else:
                    page_to_id[current_title] = [page_id]
                id_to_page[page_id] = current_title
                page_id += 1
            if line_count % print_interval == 0:
                progressBar.print_progress(line_count)
            line_count += 1

    print(' DONE')
    print(util.pretty_number(len(id_to_page)), 'titles found\n')

    print('Sorting ids for each page titles')
    for k, v in page_to_id.items():
        page_to_id[k] = sorted(v)

    print('Sorting id to page array')
    id_to_page = sorted(id_to_page.items())

    print('Saving id to page array to', ID_TO_PAGE_FILENAME)
    util.save_id_to_page(ID_TO_PAGE_FILENAME, id_to_page)


    in_page = False
    in_text = False
    words = None
    page_title = None
    page_id = 1

    re_text_start = '^.*<text.*>(.+)$'
    re_text_end = '^(.*)</text>'
    re_text_start_end = '^.*<text.*>(.+)</text'

    words_appearance = dict()

    fd_links = open(os.path.join(PAGE_LINKS_FILENAME), 'w')

    line_count = 0
    progressBar.reset_time()

    print('\nCollecting text of each page in file')
    with open(wiki_dump_filename, 'r') as fd_wiki_dump:
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
                        if page_title and words:
                            links = extract_links(page_id, words, page_to_id)
                            for link in links :
                                fd_links.write('{}\t{}\n'.format(page_id, link))

                            words_id = extract_words_id(words, word_to_id)
                            if len(words_id) > 0:
                                append_to_words_appearance(
                                    words_appearance,
                                    page_id,
                                    page_title,
                                    words_id,
                                    word_to_id,
                                    pages_per_word
                                )
                        page_id += 1
                        words = None
                        page_title = None
                        in_page = False
                    elif '<title' in line:
                        line = util.lower_and_no_accent(line)
                        match = re.match(re_title, line)
                        if match is None or ':' in match.group(1):
                            continue
                        page_title = match.group(1)
                        page_title = util.normalize_text(page_title)
                    elif '<text' in line and '</text' in line:
                        match = re.match(re_text_start_end, line)
                        if match is None:
                            continue
                        words = match.group(1)
                    elif '<text' in line:
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

    print('Saving words appearance to', WORDS_APPEARANCE_FILENAME)
    util.save_words_appearance(WORDS_APPEARANCE_FILENAME, words_appearance)

    print('\n== OUTPUT FILES ==')
    print('{} : contains id -> page title relation'.format(ID_TO_PAGE_FILENAME))
    print('{} : contains page id -> links page id'.format(PAGE_LINKS_FILENAME))
    print('{} : contains word id -> list(page id)'.format(WORDS_APPEARANCE_FILENAME))