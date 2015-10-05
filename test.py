import blockspring
import json
import sys


'''
This method uses blockspring to fetch a category of articles and write their content to a file named after the variable category 
'''
category = "Physics"


titleList = list(blockspring.runParsed("get-wikipedia-articles-in-category",{ "category": category, "limit": 500 }).params.values())

categoryList = titleList[0]
articleFile = open(category,'w+')


countFound = 0
countNotFound = 0
for category in categoryList:
	text = blockspring.runParsed("get-wikipedia-article-content", { "title": category, "parse": True }).params
	try:
		content = text['content'].encode('UTF-8')

		articleFile.write(content)
		countFound+=1

	except:
		print(category)
		countNotFound+=1
		continue
articleFile.close()


print("Found articles ", countFound)
print("Not found ",countNotFound)
