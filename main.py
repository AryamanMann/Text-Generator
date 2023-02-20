import re
import random
from nltk import WhitespaceTokenizer, trigrams
from collections import Counter


def tokenize(corpus):
    with open(corpus) as f:
        text = f.read()
        return WhitespaceTokenizer().tokenize(text)


def generate_trigrams(token):
    trigrams_ = trigrams(token)
    trigrams_list = [' '.join(x) for x in trigrams_]
    return trigrams_list


def generate_dictionary(list_of_trigrams):
    new_dict = {}
    for word in list_of_trigrams:
        new_dict.setdefault(word[0], []).append(word[1])
    return new_dict


def is_starting_word(word):
    starting_word_template = "^[A-Z]+[a-z']+.[^.?!]$"
    return bool(re.match(starting_word_template, word))


def is_ending_word(word):
    ending_word_template = ".*[?!.]"
    return bool(re.match(ending_word_template, word))


filename = input()
list_of_tokens = tokenize(filename)
trigrams_in_corpus = generate_trigrams(list_of_tokens)
lst = [(obj.split()[0] + ' ' + obj.split()[1], obj.split()[2]) for obj in trigrams_in_corpus]
data = generate_dictionary(lst)
starting_words = [word[0] for word in lst if is_starting_word(word[0])]
for i in range(20):
    sentence = list()
    first_word = random.choice(starting_words)
    sentence.append(first_word)
    while True:
        tail = data[first_word]
        freq_tail = Counter(tail)
        tail_weights = [freq_tail[value] for value in tail]
        second_word = ''.join(random.choices(tail, weights=tail_weights))
        if len(sentence) >= 4 and is_ending_word(sentence[-1]):
            break
        sentence.append(second_word)
        first_word = first_word.split()[1] + " " + second_word
    print(str(i + 1) + ") " + " ".join(sentence))
