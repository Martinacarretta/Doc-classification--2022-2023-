#This group is composed by Martina Carretta (niu:1673930) and Meritxell Carvajal (niu: 1671647)
import os 
#Exercise 1
def DocClass_Welcome ():
    print('''Document Classification is typically used in Document Processing for
assigning categories to documents. Thus, it eases their posterior
processing and analysis.

The program “DocumentClassification” classifies an input folder
containing documents in txt format. It will also receive a file
containing information about the topics to classify.

The program will generate the following files:
A txt file containing the category of the documents
A txt file containing the statistics of the classification
''')

#Exercise 2 - function that makes 2 listes: one of categories and one of keywords
def Read_Categories_Keywords (path, filename): 
    doc = open (path + '/' + filename, 'r')
    LCategories = [] #we create a list for categories
    LKeywords = [] #we create a list for the keywords of each category (NESTED LISTS)
    LKeywords2 = []
    for tline in doc: #to check each line
        i = 0
        j = 1
        while tline[j] != ':': #we read every character until we find :
            j += 1
        category = tline[i:j] #we will get from the beggining of the line until the ':' which will be each category
        LCategories.append(category) #we add the category to the categories list
        continuar = True #We do this loop until it changes line 
        while continuar == True: #we look for keywords
            i = j + 1 #we look for a new word
            while tline[i] == ' ': #we add 1 to i until we find a character different from space
                i += 1
            if tline[i] == '\n': #in case we get to the end of the line, we end the loop and add the list to the list of keywords
                continuar = False
                LKeywords.append(LKeywords2)
                LKeywords2 = []
            else: #if we find a character (another word) we position the j after i 
                j = i + 1
                while j < len(tline) and tline[j] != ' ' and tline[j] != '\n': #we look for the entire word until we find a space
                    j += 1
                keyword = tline[i:j]
                LKeywords2.append(keyword) #we add the word to the second list of keywords2 
                if j < len(tline) and tline[j] == '\n': #We get to the end of the line, we end the loop and add the list to the list of keywords2 to the original one
                    continuar = False
                    LKeywords.append(LKeywords2)
                    LKeywords2 = []
                elif j == len(tline): #We get to the end of the line and there is no intro (AKA, end of doc)
                    continuar = False
                    LKeywords.append(LKeywords2)
                    LKeywords2 = []
    doc.close()
    return LCategories, LKeywords
    
#Exercise 3 - function that makes a list of all the words from the document we want to process
def Document_Reader (path, foldername, filename):
    doc = open (path + '/' + foldername + '/' + filename, 'r')
    LWords = []
    badcharacters = '.?"“”,-–!:;()[]…/’*' + chr(39)
    word = ''
    for tline in doc:
        i = 0
        while i < len(tline):
            if tline[i] != ' ' and tline[i] != '\n' and (65>ord(tline[i]) or ord(tline[i])>90) and tline[i] not in badcharacters: #so it's a normal letter
                word += tline[i] #we add to the non definitive word
            if 65<=ord(tline[i])<=90: #if it's an uppercase letter, we transform it to lowercase and add it to word
                word += chr(ord(tline[i])+32)            
            if tline[i] == ' ' or tline[i] == '\n'  or i==len(tline)-1 or tline[i] in badcharacters: #if it's a space, an enter or the last character in the doc
                if word != '': #there could be cases where the line is empty (+enter) or that a symbol is by it's own
                    LWords.append(word) #add the word (which may have been edited)
                    word = '' #empty the variable so another word can be read
            i += 1 #next character
    doc.close()
    return LWords

#Exercise 4 - function that counts how many times is every keyword in the list of words
def Count_Frequencies(LWords, LCategories, LKeywords):
    LFrequencies = []
    for i in range (0, len(LKeywords), 1):
        LFrequencies2 = []
        for j in range (0, len(LKeywords[i]), 1):
            LFrequencies2.append(0)
        LFrequencies.append(LFrequencies2)
    #here we have set the list and how many nested lists there are
    for element in LWords: #now we chec the words from LWords. If they are in the list of keywords, we add 1 to the index
        for i in range (0, len(LKeywords), 1):
            for j in range (0, len(LKeywords[i]), 1): #we have to check every nested list, otherwise, every nested list is counted as a unique element an no word would be the same
                if element == LKeywords[i][j]:
                    LFrequencies [i][j] += 1
    return LFrequencies

#Exercise 5 - function that counts the frequence of each category and returns the position of the most repeated category
def Classify_Doc (LFrequencies):
    LVotes = []
    for i in range (0, len(LFrequencies), 1):
        count = 0
        for j in range (0, len(LFrequencies[i]), 1):
            count += LFrequencies[i][j] #we add the value of the element of the nested list
        LVotes.append(count) #we have added all the values
    max = LVotes[0]
    posMaxCat = 0
    for i in range (1, len(LVotes), 1): #we check what is the max
        if LVotes [i] > max:
            max = LVotes[i] #we update the max
            posMaxCat = i #we need to update the position
    return LVotes, posMaxCat

def rightpath (path): #check if the path exists
    correctpath = False
    if os.path.exists(path):
        correctpath = True
    return correctpath

def rightfile (filename, path): #check if the filename exists in the path
    correctfile = False
    if filename in os.listdir(path): ##it checks if the file exists in the folder
        if filename[-4:] == '.txt':
            doc = open (filename, 'r')
            empty = True
            for tline in doc: #we check if there are any lines
                for i in range (0, len(tline),1):
                    if 32 <= ord(tline[i]) <= 255: #that contain letters
                        empty = False
            if empty == False:
                correctfile = True #if there is content, it's a valid file
        else:
            raise FileNotFoundError
    else:
        raise FileNotFoundError
    return correctfile

def rightfolder (folder, path):
    correctfolder = False
    txtfile = 0
    if folder in os.listdir(path): #it checks if the folder exists in the path of the outside folder
        while txtfile == 0:
            for element in os.listdir(path): #for every file in the folder
                if element[-4:] == '.txt': #we check if it's txt file
                        txtfile = 1
        if txtfile != 0: #if there is any txt file, the path is correct
            correctfolder = True
    else:
        raise FileNotFoundError
    return correctfolder
    

#MAIN PROGRAM - CHECK THE PATHS, FILES AND FOLDERS ARE CORRECT    
DocClass_Welcome () #we call function 1

path = input('Write the path of the file that contains the definition of the categories and keywords: ') #we ask the path
correctpath = rightpath (path) #we call the function to know if it exists
while correctpath == False: #if it doesn't exist, it will be asked again until a correct path is introduced
    path = input('Write the path of the file that contains the definition of the categories and keywords: ')
    correctpath = rightpath (path)
continuar = True
while continuar == True:
    filename = input('Write the name of the file that contains the definition of the categories and keywords: ')
    try:
        correctfile = rightfile(filename, path) #we check if the file exists in the path and if it has a non empty txt file
        if correctfile == True: #if it exists and it's not empty, 
            continuar = False #we get out of the loop
    except FileNotFoundError:
        continuar = True #maybe it is not txt type
LCategories, LKeywords = Read_Categories_Keywords (path, filename) #we check the categories in the doc
print (LCategories, LKeywords)

path2 = input('Write the path of the folder that contains the document files to be processed: ')
correctpath = rightpath (path2) #we call the function to know if it exists
while correctpath == False: #if it doesn't exist, it will be asked again until a correct path is introduced
    path2 = input('Write the path of the folder that contains the document files to be processed: ')
    correctpath = rightpath (path2)
continuar = True
while continuar == True:
    foldername = input('Write the name of the folder that contains the the document files to be processed: ')
    try:
        correctfolder = rightfolder (foldername, path2) #we check if the file exists in the path and if it has a non empty txt file
        if correctfolder == True: #if it exists and it's not empty,
            continuar = False #we get out of the loop
    except FileNotFoundError:
        continuar = True #the folder is not in the path

totaltxtfiles = 0 #This will be used in statistcs
Ltop10f = [] #this list has all the frequencies of the category of each doc
Ltop10w = [] #this one has the keywords

for element in os.listdir(path2 + '/' + foldername): #for each file in the folder
    if '.txt' in element: #if it's a txt file we proceed normal
        totaltxtfiles += 1 #we add one to the counter of txt files to make percentages of the categories
        LWords = Document_Reader (path2, foldername, element) #We call function 3
        LFrequencies = Count_Frequencies(LWords, LCategories, LKeywords) #We call function 4
        #this is for top10
        for i in range (0, len(LFrequencies), 1):
            for j in range (0, len(LFrequencies[i]), 1):
                if LKeywords [i][j] in Ltop10w: #it means the keyword has already been registered so
                    for k in range (0, len(Ltop10w), 1):
                        if LKeywords [i][j] == Ltop10w [k]:
                            pos = k #we check in what position is the word in Ltop10w so we update the frequence in the correspondant position
                    Ltop10f[pos] += LFrequencies [i][j]
                else: #the word has to be registered
                    Ltop10w.append(LKeywords[i][j]) #we add that word
                    Ltop10f.append(LFrequencies [i][j]) #we add its frequence
            
        LVotes, posMaxCat = Classify_Doc (LFrequencies) #Wecall function 5        
        #we open the file where the results will be placed
        doc = open (foldername + '_DocClassification.txt', 'a') #we write in the doc
        a = '' #we add the frequencies of the keyowrds of its category
        for i in range (0, len(LKeywords[posMaxCat]), 1):
            a += (str(LKeywords[posMaxCat][i]) + ': ' + str(LFrequencies[posMaxCat][i])) #we add, of the category, keywords and their frequence
            if i == len(LKeywords[posMaxCat])-1 and element != (os.listdir(path2 + '/' + foldername)[-1]): #end of line
                a += '\n'
            elif i < len(LKeywords[posMaxCat])-1:
                a += ', '
        doc.write(element + ': ' + LCategories[posMaxCat] + ' ' + a) #we write every info of the doc (name, category, keywords and frequencies)
        doc.close()
    else: #This happens if it's not a txt file
        doc = open (foldername + '_DocClassification.txt', 'a')
        a = 'Attention: the following non txt file has been detected: ' + element
        doc.write(a)
        doc.close()
        
#MAIN PROGRAM - statistics_calculate
doc = open (foldername + '_DocClassification.txt', 'r') #we now open the document with all the processed docs and their categories
percentagecat = [] #list of percentage of each category
#percentage of each category
for element in LCategories: #we have a list of as many elements as many categories we have
    percentagecat.append(0)
for tline in doc: #we are gonna select the category
    i = 0
    while tline[i] != ' ': #we want to find the word after the space
        i += 1
    i += 1 #we don't want the space, so we add one to the position
    j = i
    while tline[j] != ' ': #we now go to the end of the word
        j += 1
    category = tline[i:j] #this is the category of the doc.txt
    for k in range (0, len(LCategories), 1): #now we check which position does the category have in the list of LCategories
        if LCategories[k] == category:
            percentagecat[k] += 1 #we add 1 to that position of the list of percentages      
#top10
for i in range (0, len(Ltop10f), 1): #we sort Ltop10f and Ltop10W 
    for j in range (0, len(Ltop10f)-i-1, 1):
        if Ltop10f[j] > Ltop10f[j+1]:
            (Ltop10f[j], Ltop10f[j+1]) = (Ltop10f[j+1], Ltop10f[j])
            (Ltop10w[j], Ltop10w[j+1]) = (Ltop10w[j+1], Ltop10w[j])
 
#MAIN PROGRAM - statistics_write
doc = open (foldername + '_DCStatistics.txt', 'a') #we write the statistics in the document
doc.write('Statistics' + '\n' + 'Total txt files: ' + str(totaltxtfiles) + '\n')
a = ''
for i in range (0, len(LCategories), 1): #for every category
    per = (percentagecat[i]/totaltxtfiles)*100 #we calculate the percentage
    a += (LCategories[i] + ': ' + str("%.2f" % (per) + '%') + '\n') #we have now written the percentage of each category with 2 decimals
doc.write(a)
doc.write('Top 10 keywords ' + str(Ltop10w[-1]) + ', '+ str(Ltop10w[-2]) + ', '+ str(Ltop10w[-3]) + ', '+ str(Ltop10w[-4]) + ', '+ str(Ltop10w[-5]) + ', '+ str(Ltop10w[-6]) + ', '+ str(Ltop10w[-7]) + ', '+ str(Ltop10w[-8]) + ', '+ str(Ltop10w[-9]) + ', '+ str(Ltop10w[-10]) + '.')
doc.close()