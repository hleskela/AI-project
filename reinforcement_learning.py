"""
This class is intended to take care of the reinforcement learning.
It uses a naive approach where it tries to match a category based
on a simple policy that we constructed.
"""
import nltk
from nltk.util import ngrams
from nltk import bigrams
from operator import add

WORDS_TO_CHECK = 20
CATEGORIES = ["Physics", "Mathematics", "Medicine", "History", "Sports", "Psychology", "Biology", "Philosophy", "Computing"]

def iterative_learning(alpha, beta, correct_category, text_to_analyze):
    """
    iterative_learning is the method that brute forces its way to a local
    (and potentially global) maximum for correctly determining the category
    """
    #Call get_word_statistics(text_to_analyze)
    return alpha * beta * correct_category * text_to_analyze

def best_matching_category(text_to_test, words_to_check):
    """
    return the max score matching from the categories and category_to_test
    """
    category_scores = []
    for category in CATEGORIES:
        current_category_score = 0
        freq_dist_cat = word_statistics(category).most_common(words_to_check)
        only_words = [str(i[0]) for i in freq_dist_cat]
        for word in text_to_test:
            if word[0] in only_words:
                current_category_score += 1
        category_scores.append(current_category_score)
    #print(category_scores)
    return (category_scores.index(max(category_scores)), category_scores)

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

def word_statistics_bigram(file):
    f = open(file)
    raw = f.read()
    array = [x.strip() for x in raw.split(',')]
    return array


def create_bigram(file):
    f = open(file)
    raw = f.read()
    tokenized_words = nltk.tokenize.word_tokenize(raw)
    pairs = [ "".join(pair) for pair in nltk.bigrams(tokenized_words)]
    with open(file + "_ngram", "a+") as ngram_file:
        # Convert all of the items in lst to strings (for str.join)
        lst = map(str, pairs)
        # Join the items together with commas
        line = " ".join(pairs)
        # Write to the file
        ngram_file.write(line)
    ngram_file.close
    f.close

def training_statistics(subjects):
    freq_dist_subjects = []
    for s in subjects:
        freq_dist_subjects.append(word_statistics(s))

    for f in freq_dist_subjects:
        print(f.most_common(WORDS_TO_CHECK))

def correctly_matched_categories(category):
    score = 0





testList = ["Integral","Polynomial", "Particle","Special Relativity", "Hospital", "French Revolution",
            "Manchester United", "Evolution", "Freudianism", "Aristotle", "Alan Turing",
            "Ancient Greece", "Babylon", "Socrates", "Alfred Adler", "Albert Einstein", "Andrew Wiles",
            "NHL", "Elephant", "Napoleon", "Michael Jordan", "Hashmap", "Health care", "CERN", "Genghis Khan",
            "Lacrosse", "Niels Bohr", "Richard Feynman", "Andromeda Galaxy", "William James", "Bobsleigh",
            "Gene", "DNA", "Charles Darwin", "Torus", "Abstract algebra", "Riemann surface",
            "Second World War", "Ancient Rome", "Pharmaceutical Drug", "Vaccine", "World Health Organization", "St Augustine",
            "Baruch Spinoza", "Random-access memory"]

correctCategories = ["Mathematics", "Mathematics", "Physics", "Physics", "Medicine", "History",
                     "Sports", "Biology", "Psychology", "Philosophy", "Computing", "History",
                     "History", "Philosophy", "Psychology", "Physics", "Mathematics", "Sports",
                     "Biology", "History", "Sports", "Computing", "Medicine", "Physics", "History",
                     "Sports", "Physics", "Physics", "Physics", "Psychology", "Sports", "Biology",
                     "Biology", "Biology", "Mathematics", "Mathematics", "Mathematics", "History",
                     "History", "Medicine", "Medicine", "Medicine", "Philosophy", "Philosophy", "Computing"]

def test_printing_words(prefix):
    a = 0
    total_correct = 0
    for text in testList:
        file = text + prefix
        word_stat = word_statistics(file).most_common(WORDS_TO_CHECK)
        best_cat_tuple = best_matching_category(word_stat)
        best_match = CATEGORIES[best_cat_tuple[0]]
        if(best_match == correctCategories[a]):
            total_correct += 1
        #print(text + " = " + best_match)
        print(best_match +" => " + correctCategories[a])
        a+=1
    print("Total score (out of 45) = " + str(total_correct))
    #for cat in CATEGORIES:
    #    print(word_statistics(cat).most_common(WORDS_TO_CHECK))
"""
test_printing_words()
word_stat = word_statistics("Integral_nouns").most_common(WORDS_TO_CHECK)
best_matching_category(word_stat)
"""

def category_decider(file, words_to_check):
    word_stat = word_statistics(file).most_common(words_to_check)
    best_cat_tuple = best_matching_category(word_stat, words_to_check)
    best_match = CATEGORIES[best_cat_tuple[0]]
    #return best_match
    return best_cat_tuple

def create_bigrams():
    for text in testList:
        file = text+"_nouns"
        create_bigram(file)
"""
bigram_array = word_statistics_bigram("Integral_nouns_ngram")
print(bigram_array)
tokenized_words = nltk.tokenize.word_tokenize(bigram_array)
tokenized_words.most_common(WORDS_TO_CHECK)
"""
#create_bigrams()

def heuristic(file, words_to_check_uni, words_to_check_bi):
    #category should be what unigrams and bigrams says it is.
    #if they match, perfect!
    #if they differ, then one of the two should be valued more and decide.
    # above can differ between iterations to see which gives the best score
    #
    # so perhaps the category function is something like this:
    # if (cat(unigram) == cat(bigram))
    #    return cat(unigram) or bigram, doesnt matter
    #else:
    # return one of these, based on some deciding factor that we can change.
    # or perhaps compare the arrays with the score for each category, and pick
    # the one with the highest total score together.
    #
    # the number of words used for unigrams and digrams should be two different
    # values, which we will alter to see which combination of values gives the
    # most correct categories
    unigram_category = category_decider(file+"_nouns", words_to_check_uni)
    bigram_category = category_decider(file+"_nouns_ngram", words_to_check_bi)
    if(unigram_category[0] == bigram_category[0]):
        return CATEGORIES[unigram_category[0]]
    else:
        #return CATEGORIES[unigram_category[0]]
        category_scores = map(add, unigram_category[1], bigram_category[1])
        category_index = category_scores.index(max(category_scores))
        return CATEGORIES[category_index]
        # this should be the sum of array thingy sarah knows
    # test_printing_words("_nouns")
    # test_printing_words("_nouns_ngram")

def brute_force_rl():
    max_score = 0
    max_x = 0
    max_y = 0
    # for x in range(10,101,10):
    for x in range(10, 11):
        for y in range(10, 11):
            a = 0
            total_correct = 0
            for file in testList:
                best_match = heuristic(file, x, y)
                if(best_match == correctCategories[a]):
                    total_correct += 1
                a+=1
            if(max_score < total_correct):
                max_score = total_correct
                max_x = x
                max_y = y
    return [max_score, max_x, max_y]

print(brute_force_rl())
