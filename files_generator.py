"""
This class is intended to take care of the reinforcement learning.
It uses a naive approach where it tries to match a category based
on a simple policy that we constructed.
"""
import nltk
from Re_SKclassifier import TextClassifier

WORDS_TO_CHECK = 20

CATEGORIES = ["Physics", "Mathematics", "Medicine", "History",
              "Sports", "Psychology", "Biology", "Philosophy", "Computing"]

testList = ["Integral", "Polynomial", "Particle", "Special Relativity",
            "Hospital", "French Revolution", "Manchester United",
            "Evolution", "Freudianism", "Aristotle", "Alan Turing",
            "Ancient Greece", "Babylon", "Socrates", "Alfred Adler",
            "Albert Einstein", "Andrew Wiles", "NHL", "Elephant",
            "Napoleon", "Michael Jordan", "Hashmap", "Health care",
            "CERN", "Genghis Khan", "Lacrosse", "Niels Bohr",
            "Richard Feynman", "Andromeda Galaxy", "William James",
            "Bobsleigh", "Gene", "DNA", "Charles Darwin", "Torus",
            "Abstract algebra", "Riemann surface", "Second World War",
            "Ancient Rome", "Pharmaceutical Drug", "Vaccine",
            "World Health Organization", "St Augustine",
            "Baruch Spinoza", "Random-access memory"]

correctCategories = ["Mathematics", "Mathematics", "Physics", "Physics",
                     "Medicine", "History", "Sports", "Biology", "Psychology",
                     "Philosophy", "Computing", "History", "History",
                     "Philosophy", "Psychology", "Physics", "Mathematics",
                     "Sports", "Biology", "History", "Sports", "Computing",
                     "Medicine", "Physics", "History", "Sports", "Physics",
                     "Physics", "Physics", "Psychology", "Sports", "Biology",
                     "Biology", "Biology", "Mathematics", "Mathematics",
                     "Mathematics", "History", "History", "Medicine",
                     "Medicine", "Medicine", "Philosophy", "Philosophy",
                     "Computing"]


class files_generator:
    def best_matching_category(self, text_to_test, words_to_check):
        """
        return the max score matching from the categories and category_to_test
        """
        category_scores = []
        for category in CATEGORIES:
            current_category_score = 0
            freq_dist_cat = self.word_statistics(category).most_common(words_to_check)
            only_words = [str(i[0]) for i in freq_dist_cat]
            for word in text_to_test:
                if word[0] in only_words:
                    current_category_score += 1
            category_scores.append(current_category_score)
        # print(category_scores)
        return (category_scores.index(max(category_scores)), category_scores)

    def histogram(self, words):
        freq = {}
        for w in words:
            if freq.has_key(w):
                freq[w] = freq[w] + 1
            else:
                freq[w] = 1
        return freq

    def word_statistics(self, file):
        """
        returns a nltk FreqDist that you can get statistics from
        """
        f = open(file)
        raw = f.read()
        tokenized_words = nltk.tokenize.word_tokenize(raw)
        frequency_distribution = nltk.FreqDist(tokenized_words)

        return frequency_distribution

    def word_statistics_bigram(self, file):
        f = open(file)
        raw = f.read()
        array = [x.strip() for x in raw.split(',')]
        return array

    def create_bigram(self, file):
        f = open(file)
        raw = f.read()
        tokenized_words = nltk.tokenize.word_tokenize(raw)
        pairs = ["".join(pair) for pair in nltk.bigrams(tokenized_words)]
        with open(file + "_ngram", "a+") as ngram_file:
            # Convert all of the items in lst to strings (for str.join)
            lst = map(str, pairs)
            # Join the items together with commas
            line = " ".join(lst)
            # Write to the file
            ngram_file.write(line)
        ngram_file.close
        f.close



    def training_statistics(self, subjects):
        freq_dist_subjects = []
        for s in subjects:
            freq_dist_subjects.append(self.word_statistics(s))

        for f in freq_dist_subjects:
            print(f.most_common(WORDS_TO_CHECK))

    def test_printing_words(self, prefix):
        a = 0
        total_correct = 0
        for text in testList:
            file = text + prefix
            word_stat = self.word_statistics(file).most_common(WORDS_TO_CHECK)
            best_cat_tuple = self.best_matching_category(word_stat)
            best_match = CATEGORIES[best_cat_tuple[0]]
            if(best_match == correctCategories[a]):
                total_correct += 1
            # print(text + " = " + best_match)
            print(best_match + " => " + correctCategories[a])
            a += 1
        print("Total score (out of 45) = " + str(total_correct))
        # for cat in CATEGORIES:
        #    print(word_statistics(cat).most_common(WORDS_TO_CHECK))
    """
    test_printing_words()
    word_stat = word_statistics("Integral_nouns").most_common(WORDS_TO_CHECK)
    best_matching_category(word_stat)
    """

    """
    bigram_array = word_statistics_bigram("Integral_nouns_ngram")
    print(bigram_array)
    tokenized_words = nltk.tokenize.word_tokenize(bigram_array)
    tokenized_words.most_common(WORDS_TO_CHECK)
    """
    # create_bigrams()

    def generator(self):
        print("\nCreating _nouns....")
        tc = TextClassifier()
        tc.createTestData(testList)
        print("... Done!")
        print("Creating Bigram files... ")
        for text in testList:
            self.create_bigram(text + '_nouns')
        print("... Done!")
