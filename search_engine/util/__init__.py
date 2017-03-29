# coding=utf-8

import itertools
import sys
import time
import pandas


def lower_and_no_accent(text):
    """
    Remove accents and some special characteres
    :param text:
    :return:
    """
    chars = {
        '’': '\'',
        'ù': 'u', 'û': 'u', 'ü': 'u', 'Ù': 'u', 'Û': 'u', 'Ü': 'u',
        'ÿ': 'y', 'Ÿ': 'y',
        'à': 'a', 'â': 'a', 'À': 'a', 'Â': 'a',
        'ç': 'c', 'Ç': 'c',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'É': 'e', 'È': 'e', 'Ê': 'e', 'Ë': 'e',
        'ï': 'i', 'î': 'i', 'Ï': 'i', 'Î': 'i',
        'ô': 'o', 'Ô': 'o',
        'œ': 'oe', 'æ': 'ae', 'Æ': 'ae', 'Œ': 'oe',
        '&lt;' : '', '&gt;': '',
        'l\'': '', 'd\'': '', 'j\'': '', 'n\'': '', 's\'': '', 'c\'': ''
    }

    text = text.lower()
    for k,v in chars.items():
        text = text.replace(k,v)
    return text


def normalize_text(content):
    """
    Remove unused charactere and multiple spaces form a text
    :param content:
    :return:
    """
    bad_chars = ['"', '.', ',', '{', '}', '=', '*', '[', ']', '|', '@', ':',
                 '!', '?', '%', '$', '&amp;', '&quot;', '~', '/', '<', '>', '\'\'']
    for bad in bad_chars:
        content = content.replace(bad, ' ')
    content = ' '.join(content.split())
    return content.strip()


def count_lines_in_file(filename):
    """
    Fast line count of a file
    :param filename:
    :return:
    """
    f = open(filename, 'rb')
    bufgen = itertools.takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in itertools.repeat(None)))
    return sum( buf.count(b'\n') for buf in bufgen if buf )


def pretty_number(n):
    """
    String representation with space each 3 characteres
    :param n: number
    :return: pretty string representation
    """
    a = str(n)[::-1]
    return (' '.join([a[i:i + 3] for i in range(0, len(a), 3)]))[::-1]


class ProgressBar:

    def __init__(self, total):
        self.total = total
        self.last_print = ''
        self.start_time = time.time()

    def reset_time(self):
        self.start_time = time.time()

    def print_progress(self, value):
        time_diff = time.time() - self.start_time
        hours, rem = divmod(time_diff, 3600)
        minutes, seconds = divmod(rem, 60)
        if hours > 0 :
            t = "{:0>2}h {:0>2}m {:0>2}s".format(int(hours),int(minutes),int(seconds))
        else :
            t = "{:0>2}m {:0>2}s".format(int(minutes),int(seconds))

        if value == 0 :
            eta = '?'
        else:
            remaining_time = self.total * time_diff / value
            remaining_time -= time_diff
            hours, rem = divmod(remaining_time, 3600)
            minutes, seconds = divmod(rem, 60)
            if hours > 0:
                eta = "{:0>2}h {:0>2}m {:0>2}s".format(int(hours), int(minutes), int(seconds))
            else:
                eta = "{:0>2}m {:0>2}s".format(int(minutes), int(seconds))

        s = '[{percent}%] {time} - {current} / {total} - ETA: {eta} '.format(
            percent=int(100 * value / self.total),
            current=pretty_number(value),
            total=pretty_number(self.total),
            time=t,
            eta=eta
        )
        sys.stdout.write('\b' * len(self.last_print))
        sys.stdout.write('\r')
        sys.stdout.write(s)
        sys.stdout.flush()
        self.last_print = s


def load_dictionary(filename, with_word_to_id=False, with_id_to_word=False):
    """
    Load dictionary (CSV format with ',' separator)
    :param filename:
    :param with_word_to_id: need to return word_to_id
    :param with_id_to_word: need to return id_to_word
    :return: word_to_id,id_to_word OR word_to_id OR id_to_word
    """
    if not with_id_to_word and not with_word_to_id:
        return None
    dataframe = pandas.read_csv(filename)
    if with_word_to_id:
        word_to_id = {}
    if with_id_to_word:
        id_to_word = {}
    for i in range(len(dataframe)):
        if with_word_to_id:
            word_to_id[dataframe['word'][i]] = int(dataframe['id'][i])
        if with_id_to_word:
            id_to_word[int(dataframe['id'][i])] = dataframe['word'][i]
    if with_id_to_word and with_word_to_id:
        return word_to_id, id_to_word
    if with_id_to_word:
        return id_to_word
    if with_word_to_id:
        return word_to_id


def load_words_appearance(filename):
    """
    Load words appearance file (CSV format with ',' separator)
    :param filename:
    :return:
    """
    fd = open(filename, 'r')
    first_line = True
    data = {}
    for line in fd.readlines():
        if first_line:
            first_line = False
            continue
        word_id, pages = line[:-1].split(',')
        data[int(word_id)] = [int(a) for a in pages.split()]
    fd.close()
    return data


def save_words_appearance(filename, data):
    """
    Save words appearance data in CSV file format
    :param filename:
    :param data:
    :return:
    """
    with open(filename, 'w') as fd:
        fd.write('word_id,page_ids\n')
        for word_id, page_ids in data.items():
            freq,pages = zip(*page_ids)
            fd.write('{},{}\n'.format(word_id, ' '.join([str(a) for a in sorted(pages)])))


def load_page_score(filename):
    """
    Load page score file and return page's id sorted by inversed page score values
    :param filename:
    :return:
    """
    fd = open(filename, 'r')
    data = []
    for line in fd.readlines():
        id, score = line[:-1].split(' ')
        data.append((float(score), id))
    fd.close()
    page_score = [page for score,page in reversed(sorted(data))]
    return page_score


def save_pageID_to_title(filename, data):
    """
    Save id_to_page into CSV format with '@' separator
    :param filename:
    :param data:
    :return:
    """
    with open(filename, 'w') as fd:
        fd.write('id@page\n')
        for pageID, title in data:
            fd.write('{}@{}\n'.format(pageID, title))