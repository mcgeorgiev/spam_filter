import re

f = open("corpus/ham/0009.1999-12-14.farmer.ham.txt")
message = f.read()
def tokenize(message):
     message = message.lower()
     all_words = re.findall("[a-z0-9']+", message)
     return all_words

def count_words(message): # add all data in a list or something
    counts = {}

    # for message, is_spam in training set:
    for word in tokenize(message):
        if word in counts:
            counts[word][1] += 1
        else:
            counts[word] = ["ham", 1]

    return counts

count_words(message)
