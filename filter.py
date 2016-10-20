import re
import math
import json
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
    
    # set() gets distinct values
    # hacky way to deal with subject line
    message = message.lower()
    all_words = set(re.findall("[a-z0-9']+", message))
    return [word for word in list(all_words) if word != 'subject']



def count_words(file_list):
    """
    Counts all the words from a group of files
    :param file_list: List of files to be read
    :return count: dictionary of counted words
                    e.g. {'daily': [spam_count, ham_count]}
    """
    counts = defaultdict(lambda: [0,0])
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

def word_probabilities(counts, total_spam, total_ham, k=0.5):
    return [[word, (totals[0]+k)/(total_spam*2*k), (totals[1]+k)/(total_ham*2*k)] for word, totals in counts.iteritems()]


def product(number_list):
    prod = 1
    for n in number_list:
         prod *= n
    return prod         
    
    
def spam_probability(word_probabilities, message, spam_total, ham_total):
    spam_log = 0.0
    ham_log = 0.0
    for word, spam_prob, ham_prob in word_probabilities:
        if word in tokenize(message):
            #print word, spam_prob, ham_prob
            spam_log += math.log(spam_prob)
            ham_log += math.log(ham_prob)
            
        else:
           # print word, spam_prob, ham_prob
            # print word
            spam_log += math.log(1.0-spam_prob)
            ham_log += math.log(1.0-ham_prob)
        
    spam = math.exp(spam_log)
    ham = math.exp(ham_log)
    return spam/(spam+ham), ham/(spam+ham)
    

def write_to_file(PATHS):
    counts = count_words(file_names(PATHS))
    with open('probabilities.txt', 'w') as outfile:
        json.dump(counts, outfile)
       

def get_counts():
    with open('probabilities.txt') as infile:
        return json.load(infile)

        
ham_total = count_path_total(PATHS[0])
spam_total = count_path_total(PATHS[1])
counts = get_counts()        
word_probs = word_probabilities(counts, spam_total, ham_total)

message = '''It is truly incredible - People from all around the world are using
their webcams to get off. Now is your chance to watch Men and women,
boys and girls show off just for you. Best of all, it's FREE, LIVE
and UN-F*CKING-BELIEVABLE. Either peep in on the sexy activity or
participate with your own webcam! You've got to try this out!
Open Amateur Webcam Feeds are Active RIGHT NOW!!!'''

print spam_probability(word_probs, message, spam_total, ham_total)

class NaiveBayes(object):
    _spam_total = None
    _ham_total = None
    _PATHS = None
    _message = None
    
    def __init__(self, message):
        self._spam_total = count_path_total(PATHS[1]) 

