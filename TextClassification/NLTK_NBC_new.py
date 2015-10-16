import blockspring
import wikipedia
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

'''
Wikipedia API: https://pypi.python.org/pypi/wikipedia/
Blockspring: https://open.blockspring.com/bs/get-wikipedia-articles-in-category
TextBlob: http://textblob.readthedocs.org/en/dev/

TextBlob has some problems for some non-ascii characters
occuring in wikipedia articles.
All encoding changing in this file is done to remedy this.
'''


class Article:
    def create_article_file(self, category, number_of_articles):
        title_list = list(blockspring.runParsed(
            "get-wikipedia-artickles-in-category",
            {"category": category, "limit": number_of_articles}
            ).params.values())
        category_list = title_list[0]
        article_file = open(category, 'a')

        for cat in category_list:
            nyy = wikipedia.page(cat).content.encode('UTF-8')
            ny = nyy.decode('utf-8')
            article_file.write(ny)
        article_file.close

    def trian_with_full_article(self, first_category, second_category):
        with open(first_category, 'r') as category_file:
            first_text = category_file.read().replace("\n", " ")
        with open(second_category, 'r') as category_file:
            second_text = category_file.read().replace("\n", " ")

        train_data = [(first_text, first_category), (second_text, second_category)]
        print("Train data completed...")

        print("Creating Naive Bayes classifier...")
        cl = NaiveBayesClassifier(train_data)
        print("Naive Bayes finished")

        return cl

    def train_with_nouns(self, first_category, second_category):
        with open(first_category, 'r') as category_file:
            first_text = TextBlob(category_file.read().replace("\n", " "))
        with open(second_category, 'r') as category_file:
            second_text = TextBlob(category_file.read().replace("\n", " "))

        first_nouns = first_text.noun_phrases
        second_nouns = second_text.noun_phrases

        first_list = [(noun, first_category) for noun in first_nouns]
        second_list = [(noun, second_category) for noun in second_nouns]

        train_data = first_list + second_list

        print("Train data completed...")
        print("Creating Naive Bayes classifier...")
        cl = NaiveBayesClassifier(train_data)
        print("Naive Bayes finished")
        return cl

    def test_with_articles(self, classifier):
        test_article = wikipedia.page("Integral").content
        print(classifier.classify(test_article))

        test_article = wikipedia.page("Special Relativity").content
        print(classifier.classify(test_article))

        test_article = wikipedia.page("Polynomial").content
        print(classifier.classify(test_article))

        test_article = wikipedia.page("Thermodynamics").content
        print(classifier.classify(test_article))

        test_article = wikipedia.page("Space").content
        print(classifier.classify(test_article))

    def test_accuracy_of_word_classification(self, classifier):
        test = [
            ('Atom', 'Physics'),
            ('Variable', 'Mathematics'),
            ('Integral', 'Mathematics'),
            ('Constant', 'Mathematics'),
            ('Equation', 'Mathematics'),
            ('Relativity', 'Physics'),
            ('Space', 'Physics'),
            ('Mechanics', 'Physics')
        ]
        print(classifier.accuracy(test))


test_article = Article()
print("Creating files.....")
test_article.create_article_file("Physics", 2)
print("First file created...")
test_article.create_article_file("Mathematics", 2)
print("All files created...")
classifier = test_article.train_with_nouns("Physics", "Mathematics")
print("Testing...")
test_article.test_with_articles(classifier)
