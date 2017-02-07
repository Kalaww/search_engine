import unidecode

def process_word(word):
    """
    Remove accent and transform to lower case
    :param word:
    :return:
    """
    return unidecode.unidecode(word).lower()