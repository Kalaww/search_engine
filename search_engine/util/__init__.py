import unidecode
import itertools
import sys
import time

def process_word(word):
    """
    Remove accent and transform to lower case
    :param word:
    :return:
    """
    return unidecode.unidecode(word).lower()

def normalize_text(content):
    """
    Remove unused charactere and multiple spaces form a text
    :param content:
    :return:
    """
    bad_chars = ['"', '.', ',', '{', '}', '=', '*', '[', ']', '|', '@', ':',
                 '!', '?', '%', '$', '&amp;', '&quot;', '~', '/']
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
    f = open(filename, 'r')
    bufgen = itertools.takewhile(lambda x: x, (f.read(1024*1024) for _ in itertools.repeat(None)))
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