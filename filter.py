import re
from os import listdir
from collections import defaultdict

PATHS = ("corpus/ham/", "corpus/spam/")

def file_names(paths):
    file_list = []
    for path in paths:
        files = listdir(path)
        files = [path+file for file in files]
        file_list += files
    return file_list

def count_path_total(path):
        return len(listdir(path))

def is_spam(path):
    items = path.split('/') # assumes that it is in the correct folder
    return items[1] == 'spam'


def tokenize(message):
    """Very basic tokenization. Does not get rid of number words and does not deal with the subject/body."""
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return all_words


def count_words(file_list):
    """
    Counts all the words from a group of files
    :param file_list: List of files to be read
    :return count: dictionary of counted words
                    e.g. {'daily': [spam_count, ham_count]}
    """
    counts = {}#defaultdict(lambda: [0,0])
    for file_name in file_list:
        with open(file_name, 'r') as f:
            message = f.read()

        for word in tokenize(message):
            if word in counts:
                if is_spam(file_name):
                    counts[word][0] += 1
                else:
                    counts[word][1] += 1

            else:
                if is_spam(file_name):
                    counts[word] = [1,0]
                else:
                    counts[word] = [0,1]

    return counts

def word_probabilities(counts, total_spam, total_ham):
    # CONSTANTS
    # P(spam)
    S = total_spam/(total_spam+total_ham*1.0)
    # P(notspame)
    notS = total_ham/(total_spam+total_ham*1.0)

    for word, totals in counts.iteritems():
        # P(word)
        W = (totals[0])/(total_spam*1.0)
        print (W*S)/S







ham_total = count_path_total(PATHS[0])
spam_total = count_path_total(PATHS[1])

counts = count_words(file_names(PATHS))

word_probabilities(counts, spam_total, ham_total)



