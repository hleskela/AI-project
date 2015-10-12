import blockspring
import wikipedia
import sklearn
import sys
import json
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer


reload(sys)
sys.setdefaultencoding('utf8')



class TextClassifier():

	def __init__(self):
		self.categories = None

	def get_nouns(self, nouns, articleFile):
		for noun in nouns:
			if '=' in noun : continue
			try:
				noun.decode('ascii')
			except:
				continue
			articleFile.write(noun + " ")
			articleFile.close

	def createTrainingData(self, categories, numberOfArticles):
		for category in categories:
			print category
			titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": category, "limit": numberOfArticles }).params.values())
			categoryList = titleList[0]
			articleFile = open(category,'w+')

			for cat in categoryList:

				articleFile.write("[" + category + "] ")
				articleContent = TextBlob(wikipedia.page(cat).content.encode('UTF-8'))
				nouns = articleContent.noun_phrases
				self.get_nouns(nouns, articleFile)
				'''
				for noun in nouns:
				#Removes weird words, only writes if they are not weird.
				if '=' in noun : continue
				try:
				noun.decode('ascii')
				except:
				continue
				articleFile.write(noun + " ")

				articleFile.close
				'''




	def createTestData(self, articleList):
		for article in articleList:
			articleFile = open(article + "_test", 'w+')
			article_nouns = open(article + "_nouns", 'w+')
			articleContentTwo = TextBlob(wikipedia.page(article).content.encode('UTF-8'))
			articleContent = wikipedia.page(article).content.encode('UTF-8')
			nouns = articleContentTwo.noun_phrases
			self.get_nouns(nouns, article_nouns)
			articleFile.write(articleContent)
			articleFile.close


tc = TextClassifier()

tc.createTrainingData(["Physics", "Mathematics", "Medicine", "History", "Psychology", "Biology", "Philosophy", "Computing"], 7)
tc.createTestData(["Integral","Polynomial", "Particle","Special Relativity", "Hospital",
	    "French Revolution", "Manchester United", "Evolution", "Freudianism", "Aristotle", "Alan Turing"])

testList = ["Integral","Polynomial", "Particle","Special Relativity", "Hospital", "French Revolution",
            "Manchester United", "Evolution", "Freudianism", "Aristotle", "Alan Turing"]
testData = list()

for test in testList:
	data = open(test + "_test", "r").read()
	testData.append(data)


categories = ["Physics", "Mathematics", "Medicine", "History", "Psychology", "Biology", "Philosophy", "Computing"]

content = list()
for category in categories:
	content.append(open(category, 'r').read())

print "All data created"
vectorizer = TfidfVectorizer(max_df=2)


X = vectorizer.fit_transform(content)

classifier = MultinomialNB().fit(X, content)

print "MNB finished"
joblib.dump(classifier, 'storedMNB.pkl')

Xtest = vectorizer.transform(testData)

predicted = classifier.predict(Xtest)




#Just printing some. Ask andreas if you want to know what is going on here...
counter = 0
for doc, category in zip(testList, predicted):
	print('%r was classifed as:  %s' % (doc, str(predicted[counter].split(" ",1)[0]).replace("[", "").replace("]","")))
	counter += 1
