import json
from random import randint
import csv
import os
import sys
#settings
try:
    if sys.argv[1] == '1':
        log = True
    elif sys.argv[1] == '0':
        log = False
except:
    log = True # Do you want to log the result to a file?

try:
    if sys.argv[2] != '_':
        stage3 == sys.argv[2]
    else:
        stage3 = 70
except:
    stage3 = 70 #Treshold when to move to stage 3 (percantage of know word that needs to be known before guessing)

try:
    if sys.argv[3] != '_':
        stage2 == sys.argv[3]
    else:
        stage2 = 1000
except:
    stage2 = 1000 #Threshold when to move to stage 2 (max number of possible words for stage 2) 

try:
    if sys.argv[4] != '_':
        stage3_2 == sys.argv[4]
    else:
        stage3_2 = 10
except:
    stage3_2 = 10 #Max number of words that remain before stage 3

#load the dictionary
f = open('dictionary_compact.json',)
data = json.load(f)
keys = []
#get just the keys
for key in data: 
    keys.append(key)
print('Choosing a random word...')
word_m = keys[randint(0, len(keys))]#word with random id from keys array
print('Chosen word: ' + word_m)

#word chosen time to guess it
lenght = len(word_m)

def split(word):
    return [char for char in word]

def get_known_perc():
    return len((''.join(wip)).replace('_','')) / len(word_m)

def get_similarity(test_list1,test_list2):
    return len(set(test_list1) & set(test_list2)) / float(len(set(test_list1) | set(test_list2))) * 100

game_over = False
global mistakes
mistakes = 0

letters = ['e','t','a','o','i','n','s','h','r','d','l','c','u','m','w','f','g','y','p','b','v','k','j','x','q','z','-',] #letters in order of frequency in English
wip = [] #memory of word in assembly
wip_f = split(word_m) #finished word in array
possible_words = [] # all the possible words
attempts = 0 # moves
tried_letters = [] #wrong letters
i = 0
correct_letters = [] #correct letters

while i < lenght:
    wip.append('_') #Create the wip word with _ instead of letters
    i = i + 1

#function used in stage 1 and 2 for checking if letter is in searched word and associated game logic
def try_letter(letter):
    print('Possbile number of words: ' + str(len(possible_words)))
    if(len(possible_words) < 15):
        print('Possible words: ' + ','.join(possible_words))
    print(''.join(wip))
    print('Trying letter: ' + letter)
    #print(wip)
    #print(wip_f)
    
    if letter in wip_f:
        i2 = 0
        correct_letters.append(letter)
        for s in wip_f:
            if letter == s:
                wip[i2] = letter
                
            i2 = i2 + 1
        largest_chunk = max(''.join(wip).split('_'), key=len)
        for word in possible_words:
            if letter not in word or largest_chunk not in word:
                if(word == word_m):
                    print(word)
                #print(word + ';' + largest_chunk + ';' + letter)
                possible_words.remove(word)
    else:
        global mistakes
        mistakes = mistakes + 1
        tried_letters.append(letter)
        largest_chunk = max(''.join(wip).split('_'), key=len)
        for word in possible_words:
            if letter in word or largest_chunk not in word:
                possible_words.remove(word)
    print(''.join(wip))
    #print(possible_words)
    
#Create the most broad version of possible words possible begfore stage 1
for key in keys:
    if len(key) == lenght:
        possible_words.append(key)


#work on finding the word
#This is the logic
#__________________________________________________________________
#Stage 1 (Try and guess by average english letter frq)
#__________________________________________________________________
for letter in letters:
    if game_over == True:
        break
    if len(possible_words) == 1 and game_over != True:
        print('_____________________________________________________________________')
        print('The word is: ' + ''.join(possible_words))
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    if(''.join(wip) == ''.join(wip_f)) and game_over != True:
        print('_____________________________________________________________________')
        print('The word is: ' + ''.join(wip))
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    if len(possible_words) < stage2 and game_over != True:
        #Move to stage 2
        break
    elif letter not in tried_letters and letter not in correct_letters:
        for item in possible_words:
            i5 = 0
            for char in wip:
                if wip[i5] != '_' and item[i5] != wip[i5]:
                    possible_words.remove(item)
                    break
                i5 = i5 + 1
        print('_____________________________________________________________________')
        print('Attempt number ' + str(attempts))
        try_letter(letter)
    attempts = attempts + 1
#__________________________________________________________________
#Stage 2 (Try and guess by average english letter frq)
#__________________________________________________________________
full = len(''.join(possible_words))
totals = []
for item in letters:
    if item not in tried_letters and item not in correct_letters:
        one = sum(s.count(item) for s in possible_words)
        percentage = one / full
        row = {'letter':item,'value':percentage}
        totals.append(row)
totals = sorted(totals, key=lambda k: k['value'], reverse=True)
for new_letter in totals:
    if game_over == True:
        break
    if len(possible_words) == 1 and game_over != True:
        print('_____________________________________________________________________')
        print('The word is: ' + ''.join(possible_words))
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    if(''.join(wip) == ''.join(wip_f)) and game_over != True:
        print('_____________________________________________________________________')
        print('The word is: ' + ''.join(wip))
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    if get_known_perc() * 100 > stage3 and game_over != True and len(possible_words) < stage3_2:
        #move to stage 3
        break
    for item in possible_words:
        i5 = 0
        for char in wip:
            if wip[i5] != '_' and item[i5] != wip[i5]:
                possible_words.remove(item)
                break
        i5 = i5 + 1
    print('_____________________________________________________________________')
    print('Attempt number ' + str(attempts))
    try_letter(new_letter['letter'])
    attempts = attempts + 1
#__________________________________________________________________
#Stage 3 (Try and guess by string similiarity)
#__________________________________________________________________
most_likely = []
for item in possible_words:
    row = {'word':item,'sim':get_similarity(wip,list(item))}
    most_likely.append(row)
most_likely = sorted(most_likely, key=lambda k: k['sim'], reverse=True)
for item in most_likely:
    if game_over == True:
        break
    if len(possible_words) == 1 and game_over != True:
        print('_____________________________________________________________________')
        print('The word is: ' + ''.join(possible_words))
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    if item['word'] == word_m and game_over != True:
        print('_____________________________________________________________________')
        print('I correctly guessed: ' + item['word'] + '(' + str(item['sim']) + ')')
        print('Mistakes I made: ' + str(mistakes))
        game_over = True
        break
    print('_____________________________________________________________________')
    print('Attempt number ' + str(attempts))
    print('I wrongly guessed ' + item['word'] + '(' + str(item['sim']) + ')')
    attempts = attempts + 1
    mistakes = mistakes + 1

if log:
    if os.path.exists('output.csv') == False:
        with open('output.csv',mode='w',newline='') as output:
            fieldnames = ['word', 'length', 'attempts', 'mistakes']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'word': word_m, 'length': len(word_m), 'attempts': attempts, 'mistakes':mistakes})
    else:
        with open('output.csv',mode='a',newline='') as output:
            fieldnames = ['word', 'length', 'attempts', 'mistakes']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writerow({'word': word_m, 'length': len(word_m), 'attempts': attempts, 'mistakes':mistakes})

try:
    if sys.argv[5] == 1 :
        input("Press any key to terminate the program")
except:
    pass


