import os
import csv
import math
import pycantonese
from pycantonese import pos_tag

#############---- Pos tagging using PyCantonese ----################
word_input = 'word.csv'
pos_tag_file = 'tagged_words.csv'
with open(word_input,'r',encoding='utf-8-sig') as file:
    lines = [line.strip().split('\t') for line in file.readlines()][1:]
words = [line[0] for line in lines]
tagged_words = pos_tag(words)
with open(output_file,'w',newline='',encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Word','POS Tag'])
    for (word, tag) in tagged_words:
        writer.writerow([word, tag])
print(f'Done pos tagging to {pos_tag_file}')

#############---- Word frequency using HKCancor as reference ----################

# Load the HKCanCor corpus
hkcancor = pycantonese.hkcancor()
freq = hkcancor.word_frequencies()

# Function to check Cantonese word frequency from unigram to 4-gram
def get_Cantonese_freq(word):
    if word in freq:
        return freq[word]
    n = len(word)
    if n == 2:
        tok1 = word[0]
        tok2 = word[1]
        if tok1 in freq and tok2 in freq:
            return freq[tok1] * freq[tok2]
    elif n == 3:
        tok1 = word[0]
        tok2 = word[1]
        tok3 = word[2]
        if tok1 in freq and tok2 in freq and tok3 in freq:
            return freq[tok1] * freq[tok2] * freq[tok3]
    elif n == 4:
        tok1 = word[0]
        tok2 = word[1]
        tok3 = word[2]
        tok4 = word[3]
        if tok1 in freq and tok2 in freq and tok3 in freq and tok4 in freq:
            return freq[tok1] * freq[tok2] * freq[tok3] * freq[tok4]
    return 0

# Calculate word frequency
words,results = [],[]
with open('word.csv', 'r') as file:
    csvreader = csv.DictReader(file, delimiter=',')
    for row in csvreader:
        word = row['\ufeffword']
        words.append(word)
for word in words:
    word_freq = get_Cantonese_freq(word)
    if word_freq != 0:
        result = math.log(word_freq + 1)
    else:
        result = 0
    results.append(result)

with open('log_freq.csv','w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Word', 'log_freq'])
    for word, result in zip(word_list, results):
        csvwriter.writerow([word, result])

print('Done word frequency count!')

