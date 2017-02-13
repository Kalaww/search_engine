import unidecode

def process_word(word):
    """
    Remove accent and transform to lower case
    :param word:
    :return:
    """
    return unidecode.unidecode(word).lower()

def normalize_page_content(content):
    bad_chars = ['"', '\'', '.', ',', '{', '}', '=', '*', '[', ']', '|', '@', ':',
                 '!', '?', '%', '$', '&amp;', '&quot;', '~', '/']
    for bad in bad_chars:
        content = content.replace(bad, ' ')
    content = ' '.join(content.split())
    return content.strip()