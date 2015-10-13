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

'''

SKlearn installation:
http://scikit-learn.org/stable/install.html

Wikipedia API: https://pypi.python.org/pypi/wikipedia/
Blockspring: https://open.blockspring.com/bs/get-wikipedia-articles-in-category
TextBlob: http://textblob.readthedocs.org/en/dev/



This program creates and tests the Multinomial Naive Bayes classifier
of SciKit. This version has a simple text user interface.


'''




class TextClassifier():

	def __init__(self, categories):

		self.classifier = None
		self.categories = categories


	def createMNB(self, content):
		vectorizer = TfidfVectorizer(max_df=1)
		X = vectorizer.fit_transform(content)
		classifier = MultinomialNB().fit(X,content)
		

		boolStore = raw_input("Do you want to save your classifier? y/n: ")
		if (boolStore == "y"): 
			classifierName = raw_input("Specify a name (Format: name.pkl): ")
			joblib.dump(classifier, classifierName) 

		self.classifier = classifier



	def messagesToUser(self):
		content = list()
		for category in self.categories:
			content.append(open(category, 'r').read())

		boolStored = raw_input("Do you want to use a stored classifier? y/n: ").lower()
		
		if (boolStored == "y"): 
			classifierName =  raw_input("Please specify the name of the stored classifier (Format: name.pkl): ")
			try: self.classifier = joblib.load(classifierName) 
			except:
				print "File not found"
				sys.exit(0)

		elif (boolStored == "n"):
			print "\nYou chose to create a new classifier."
			self.createMNB(content)

		else: 
			print "Wrong input. Exiting program..."
			sys.exit(0)


		testList = list()

		listNotFinished = True

		print "\nYou will now specify the names of the articles you want to test. Type exit when you want to finish."
		print "Make sure it is correctly spelled. If the article name consists of two words, separate them by a space."

		while(listNotFinished):

			article = raw_input("Article name: ")

			if (article == "exit"):
				listNotFinished = False
				break

			testList.append(article)


		self.createTestData(testList)

		testData = list()

		for test in testList:
			data = open(test + "_test", "r").read()
			testData.append(data)


		vectorizer = TfidfVectorizer(max_df = 1)

		vectorizer.fit_transform(content)

		X_test = vectorizer.transform(testData)


		predictions = self.classifier.predict(X_test)

		
		#Just printing some...
		counter = 0
		for doc, category in zip(testList, predictions):
			print('%r was classifed as:  %s' % (doc, str(predictions[counter].split(" ",1)[0]).replace("[", "").replace("]","")))
			counter += 1


	def createTrainingData(self, categories, numberOfArticles):
		for category in categories:
			titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": category, "limit": numberOfArticles }).params.values())
			categoryList = titleList[0]

			articleFile = open(category,'w+')
			
			for cat in categoryList:
				articleFile.write("[" + cat + "] ")
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


	def createTestData(self, articleList):
		for article in articleList:
			articleFile = open(article + "_test", 'w+')
			articleContent = wikipedia.page(article).content.encode('UTF-8')
			articleFile.write(articleContent)
			articleFile.close		
		


tc = TextClassifier(["Physics", "Mathematics", "Medicine", "History", "Sports", "Psychology", "Biology", "Philosophy", "Computing"])

tc.messagesToUser()