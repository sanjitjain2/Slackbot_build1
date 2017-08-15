import argparse

valid_words = []
l = []
dic = {}
score = 0
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,   
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}                       #dict of the scores assigned to each English alphabet

##### Argument parser 
"""parser = argparse.ArgumentParser()   
parser.add_argument("echo", help="Echo the wrack of letters", type=str)
args = parser.parse_args()
print args.echo
rack = args.echo"""

rack = raw_input('Enter rack of words: ').lower()       #taking rack of word from the user
fp = open('sowpods.txt', 'r')                           #reading SOWPODS file

for line in fp.readlines():
    flag = 0
    dup_rack = rack
    word = line.strip()                         #Handling every valid word in the file
    for letter in word.lower():
        if letter not in dup_rack:
            flag = 1
            break
        elif letter in dup_rack:
            dup_rack = dup_rack.replace(letter, '')     #removing the letter that is already checked from rack var
    if flag == 0:
        valid_words.append(word.lower())                #list of all the valid words


fp.close()
for word in set(valid_words):
    for letter in word.lower():
        score += scores[letter]                 #calculating the scores per word
    dic.update({word : score})                  #adding valid words with their scores to the dictionary 
    score = 0

if dic == {}:
    print 'No valid word found!'
else:
    print 'All the valid words are....'
    for key in sorted(dic):
        print dic[key], key                         #printing score and valid word pair from the dict
