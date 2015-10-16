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
import matplotlib.pyplot as plt


reload(sys)
sys.setdefaultencoding('utf8')



class TextClassifier():

	def __init__(self, testList, correctCategories, categories, alpha, maxfeatures):
		self.categories = categories
		self.testList = testList
		self.correctCategories = correctCategories
		self.alpha = alpha
		self.maxfeatures = maxfeatures

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


		vectorizer = TfidfVectorizer(max_features=self.maxfeatures)


		X = vectorizer.fit_transform(content)

		classifier = MultinomialNB(self.alpha).fit(X, content) 

		Xtest = vectorizer.transform(testData)

		predicted = classifier.predict(Xtest)

		#This prints the results. 
		counter = 0
		correctCounter = 0
		for category in predicted:
			predictedAsString = str(predicted[counter].split(" ",1)[0]).replace("[", "").replace("]","")
			if (predictedAsString == correctCategories[counter]): correctCounter += 1.0
			counter += 1
		accuracy = str(correctCounter/len(testList))
		return accuracy

	@staticmethod
	def createTrainingData(categories,numberOfArticles):
		for category in categories:
			print ("Category: " + str(category))
			try:
				titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": category, "limit": numberOfArticles }).params.values())[0]
			except:
				print "Error in getting articles in category."
				continue

			articleFile = open(category,'a')
			articleFile.write("[" + category + "] ")

			for cat in titleList:
				try: articleContent = TextBlob(wikipedia.page(cat).content.encode('UTF-8'))
				except: 
					print "Error in getting article"
					continue
				try: nouns = articleContent.noun_phrases
				except:
					print "Error in getting nouns"
					continue
				for noun in nouns:
					#Removes weird words, only writes if they are not weird.
					if '=' in noun : continue
					try: 
						noun.decode('ascii')
					except:
						continue
					articleFile.write(noun + " ")

			subcategories = list(blockspring.runParsed("get-wikipedia-sub-categories", { "category": category}).params.values())[0]

			for subcategory in subcategories: 
				print ("Subcategory: " + str(subcategory))
				try:
					titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": subcategory, "limit": 2 }).params.values())
				except: 
					print "Error in getting articles in subcategory"
					continue

				categoryList = titleList[0]
				
				for cat in categoryList:
					try:
						articleContent = TextBlob(wikipedia.page(cat).content.encode('UTF-8'))
					except: 
						"Error in getting article."
						continue
					try: nouns = articleContent.noun_phrases
					except:
						print "Error in getting nouns"
						continue
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

#This specifies the correct categories of the test list above, and it is used to print the accuracy of
#the classifier.

correctCategories = ["Mathematics", "Mathematics", "Physics", "Physics", "Medicine", "History",
"Sports", "Biology", "Psychology", "Philosophy", "Computing",
"History", "History", "Philosophy", "Psychology", "Physics", "Mathematics", "Sports", "Biology", "History",
"Sports", "Computing", "Medicine", "Physics", "History","Sports", "Physics", "Physics", "Physics", "Psychology", "Sports", 
"Biology", "Biology", "Biology", "Mathematics", "Mathematics", "Mathematics",
"History", "History", "Medicine", "Medicine", "Medicine", "Philosophy", "Philosophy", "Computing"]


categories = ["Physics", "Mathematics", "Medicine", "History", "Sports", "Psychology", "Biology", "Philosophy", "Computing"]


'''
Use the finished training data in the folder copy_of_train_data. Put it in the same directory as this program.
This data has been cleaned from errors in it, which may occur when one tries to get too much data from
wikipedia with blockspring. Be aware that if you choose to make your own data, you might have to
clean the files created. This could not be handled fully with try/except clauses
as far as we found. Creating new test data is not a problem, as it does not use blockspring.

'''
#TextClassifier.createTestData(testList)
#TextClassifier.createTrainingData(categories, 5)
accuracyList = list()



for maxfeatures in range(1,301):
	tc = TextClassifier(testList, correctCategories, categories,1.0,maxfeatures)
	accuracy = tc.createClassifier()
	accuracyList.append(accuracy)



maxfeatList = range(1,301)
plt.plot(maxfeatList,accuracyList, 'ro')
plt.axis([0, 301, 0, 1])
plt.ylabel('Accuracy of classifer')
plt.xlabel('Max features based on term frequency')
plt.title('Multinomial Naive Bayes classifer')
plt.show()