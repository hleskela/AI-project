import blockspring
import wikipedia
import sklearn
import sys
import json
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
import numpy as np
from scipy import arange
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer


reload(sys)
sys.setdefaultencoding('utf8')



class TextClassifier():

	def __init__(self, testList, correctCategories, categories, alpha):
		self.categories = categories
		self.testList = testList
		self.correctCategories = correctCategories
		self.alpha = alpha

	def createClassifier(self):


		categories = self.categories
		testList = self.testList
		correctCategories = self.correctCategories

		testData = list()

		for test in testList:
			data = open(test + "_test", "r").read()
			testData.append(data)

		content = list()
		for category in categories:
			content.append(open(category, 'r').read())

		print "All data created"
		vectorizer = TfidfVectorizer(min_df=1)


		X = vectorizer.fit_transform(content)

		classifier = MultinomialNB(self.alpha).fit(X, content)

		print "MNB finished"
		joblib.dump(classifier, 'storedMNB.pkl') 

		Xtest = vectorizer.transform(testData)

		predicted = classifier.predict(Xtest)

		#Just printing some. Ask andreas if you want to know what is going on here...
		counter = 0
		correctCounter = 0
		for doc, category in zip(testList, predicted):
			predictedAsString = str(predicted[counter].split(" ",1)[0]).replace("[", "").replace("]","")
			print('%r was classifed as:  %s' % (doc, predictedAsString))
			if (predictedAsString == correctCategories[counter]): correctCounter += 1.0
			counter += 1
		accuracy = str(correctCounter/len(testList))
		print ("Accuracy: " + accuracy)
		return accuracy

	@staticmethod
	def createTrainingData(categories, numberOfArticles):
		for category in categories:
			print category
			titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": category, "limit": numberOfArticles }).params.values())
			categoryList = titleList[0]
			articleFile = open(category,'w+')
			
			for cat in categoryList:

				articleFile.write("[" + category + "] ")
				articleContent = TextBlob(wikipedia.page(cat).content.encode('UTF-8'))
				nouns = articleContent.noun_phrases
				for noun in nouns:
					#Removes weird words, only writes if they are not weird.
					if '=' in noun : continue
					try: 
						noun.decode('ascii')
					except:
						continue
					articleFile.write(noun + " ")

			articleFile.close

	@staticmethod
	def createTestData(articleList):
		for article in articleList:
			articleFile = open(article + "_test", 'w+')
			articleContent = wikipedia.page(article).content.encode('UTF-8')
			articleFile.write(articleContent)
			articleFile.close		



testList = ["Integral","Polynomial", "Particle","Special Relativity", "Hospital", "French Revolution", 
	    "Manchester United", "Evolution", "Freudianism", "Aristotle", "Alan Turing", 
	    "Ancient Greece", "Babylon", "Socrates", "Alfred Adler", "Albert Einstein", "Andrew Wiles",
	    "NHL", "Elephant", "Napoleon", "Michael Jordan", "Hashmap", "Health care", "CERN", "Genghis Khan",
	    "Lacrosse", "Niels Bohr", "Richard Feynman", "Andromeda Galaxy", "William James", "Bobsleigh",
	    "Gene", "DNA", "Charles Darwin", "Torus", "Abstract algebra", "Riemann surface", 
	    "Second World War", "Ancient Rome", "Pharmaceutical Drug", "Vaccine", "World Health Organization", "St Augustine",
	    "Baruch Spinoza", "Random-access memory"]

correctCategories = ["Mathematics", "Mathematics", "Physics", "Physics", "Medicine", "History",
		     "Sports", "Biology", "Psychology", "Philosophy", "Computing",
		     "History", "History", "Philosophy", "Psychology", "Physics", "Mathematics", "Sports", "Biology", "History",
		     "Sports", "Computing", "Medicine", "Physics", "History","Sports", "Physics", "Physics", "Physics", "Psychology", "Sports", 
		     "Biology", "Biology", "Biology", "Mathematics", "Mathematics", "Mathematics",
		     "History", "History", "Medicine", "Medicine", "Medicine", "Philosophy", "Philosophy", "Computing"]



categories = ["Physics", "Mathematics", "Medicine", "History", "Sports", "Psychology", "Biology", "Philosophy", "Computing"]

tc = TextClassifier(testList, correctCategories, categories,1.0)
tc.createTestData(testList)
TextClassifier.createTrainingData(categories, 5)
"""
for alpha in arange(0.9,1.0,0.1):			#ignore this...
	
	tc = TextClassifier(testList, CorrectCategories, categories,alpha)
	#print ("Training size: " + str(trainingSize))
	tc.createClassifier()
"""
