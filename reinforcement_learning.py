"""
This class is intended to take care of the reinforcement learning.
It uses a naive approach where it tries to match a category based
on a simple policy that we constructed.
"""
import nltk

WORDS_TO_CHECK = 10


def iterative_learning(alpha, beta, correct_category, text_to_analyze):
    """
    iterative_learning is the method that brute forces its way to a local
    (and potentially global) maximum for correctly determining the category
    """
    #Call get_word_statistics(text_to_analyze)
    return alpha * beta * correct_category * text_to_analyze

def best_matching_category(categories, text_to_test):
    """
    return the max score matching from the categories and category_to_test
    """
    category_scores = []
    for category in categories:
        current_category_score = 0
        #compare top word occurences with the category_to_test
        for word in category:
            #if word occurence is within 3% of the category_to_test,add to score
            print("TODO" + word + text_to_test)
        category_scores.append(current_category_score)

    return category_scores.index(max(category_scores))

def histogram(words):
    freq = {}
    for w in words:
        if freq.has_key(w):
            freq[w] = freq[w] + 1
        else:
            freq[w] = 1
    return freq


def word_statistics(file):
    """
    returns a nltk FreqDist that you can get statistics from
    """
    f = open(file)
    raw = f.read()
    tokenized_words = nltk.tokenize.word_tokenize(raw)
    frequency_distribution = nltk.FreqDist(tokenized_words) 
    
    return frequency_distribution

def training_statistics():
    freq_dist_subjects = []
    for s in subjects:
        freq_dist_subjects.append(word_statistics(s))

    for f in freq_dist_subjects:
        print(f.most_common(WORDS_TO_CHECK))

def find_matching_category(freq_dist_categories, freq_dist_text):
    top_words_text = freq_dist_text.most_common(WORDS_TO_CHECK)
    score_categories
    for word in top_words_text:
        for cat in freq_dist_categories:
            



testList = ["Integral","Polynomial", "Particle","Special Relativity", "Hospital", "French Revolution",
            "Manchester United", "Evolution", "Freudianism", "Aristotle", "Alan Turing"]

f = open('Integral_nouns')
raw = f.read()
split = raw.split() 
freq = histogram(split)
print(freq)

f1 = open('Mathematics')
raw1 = f1.read()
words = nltk.tokenize.word_tokenize(raw1)
print(raw1)
middle = raw1.split()
split1 = nltk.FreqDist(words)
freq1 = split1.keys()
print(split1.most_common(WORDS_TO_CHECK))


training_statistics()
