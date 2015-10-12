import blockspring
import wikipedia
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

'''
Wikipedia API: https://pypi.python.org/pypi/wikipedia/
Blockspring: https://open.blockspring.com/bs/get-wikipedia-articles-in-category
TextBlob: http://textblob.readthedocs.org/en/dev/


TextBlob has some problems for some non-ascii
characters occuring in wikipedia articles.
All encoding changing in this file is done to remedy this.

'''

# reload(sys)
# sys.setdefaultencoding('utf8')


'''

The methods here could definitely be improved, for example the training
methods, which should take a category list instead of several arguments,
and the testing methods which should also be generalized.
However, as the NB classifier turned out to be very slow, we did not
spend any time on optimizing or refactoring other parts of the code as
the NLTK classifier was abandonded for other alternatives.


'''


def createFile(category, numberOfArticles):
    titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category", {"category": category, "limit": numberOfArticles}).params.values())
    categoryList = titleList[0]
    articleFile = open(category, 'w+')

    for cat in categoryList:
        nyy = wikipedia.page(cat).content.encode('UTF-8')
        print('>>>>>>>>>>>>>>>>>>>>>', type(nyy))
        ny = nyy.decode("utf-8")
        print('>>>>>>>>>>>>>>>>>>>>>', type(ny))
        articleFile.write(ny)
        print("Loading article: " + cat)
	articleFile.close


def trainWithFullArticle(category, secondCategory):
    with open(category, "r") as myFile:
        text = myFile.read().replace("\n", " ")
    with open(secondCategory, "r") as myFile:
        secondText = myFile.read().replace("\n", " ")

    train_data = [(text, category), (secondText, secondCategory)]
    print("Train data completed...")

    print("Creating Naive Bayes classifier...")
    cl = NaiveBayesClassifier(train_data)
    print("Naive Bayes finished")

    return cl


def trainWithNouns(category, secondCategory):
	with open(category, "r") as myFile:
		text = TextBlob(myFile.read().replace("\n", " "))

	with open(secondCategory, "r") as myFile:
		secondText = TextBlob(myFile.read().replace("\n", " "))

	nouns = text.noun_phrases
	secondNouns = secondText.noun_phrases

	firstList =  [(noun, category) for noun in nouns]
	secondList = [(noun, secondCategory) for noun in secondNouns]

	train_data = firstList + secondList

	print("Train data completed...")

	print("Creating Naive Bayes classifier...")
	cl = NaiveBayesClassifier(train_data)
	print("Naive Bayes finished")
	return cl


def testWithArticles(classifier):
	testArticle = wikipedia.page("Integral").content
	print(classifier.classify(testArticle))

	testArticle = wikipedia.page("Special Relativity").content
	print(classifier.classify(testArticle))

	testArticle = wikipedia.page("Polynomial").content
	print(classifier.classify(testArticle))

	testArticle = wikipedia.page("Thermodynamics").content
	print(classifier.classify(testArticle))

	testArticle = wikipedia.page("Space").content
	print(classifier.classify(testArticle))


def testAccuracyOfWordClassification(classifier):
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


print("Creating files...")

createFile("Physics", 2)

print("First file created...")

createFile("Mathematics", 2)

print("All files created...")


classifier = trainWithNouns("Physics", "Mathematics")

print("Testing...")


testWithArticles(classifier)

'''

To test the NLTK classifier, just call any of the test
methods above with the classifier.

'''
