import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import regexp

files = ['suny', 'gutenberg']

def fast_tokenizer(list_of_files, tokenizer) :
    dict = {}
    for file in list_of_files:
        f = open('four_meetings_' + file + '.txt')
        raw = f.read()
        dict[file] = tokenizer(raw)
    return dict

c = fast_tokenizer(files, word_tokenize)
ws = fast_tokenizer(files, regexp.WhitespaceTokenizer().tokenize)

#[print("{0}: {1}".format(k, len(c[k]))) for k in c]

#[print("{0}: {1}".format(k, len(ws[k]))) for k in ws]

from nltk.probability import *

cs = c['suny'] + c['gutenberg']
wss = ws['suny'] + ws['gutenberg']
total_tokens = set(cs + wss)

print("There are {0} total tokens from the combined set of texts.".format(len(total_tokens)))

c_suny_fd = FreqDist(c['suny'])
c_gutenberg_fd = FreqDist(c['gutenberg'])
ws_suny_fd = FreqDist(ws['suny'])
ws_gutenberg_fd = FreqDist(ws['gutenberg'])

filename = "word_frequencies1.csv"

f = open(filename, 'w', encoding='utf-8')
f.write("Word, suny_c, gutenberg_c, suny_ws, gutenberg_ws, total\n")
for token in total_tokens:
    total = c_suny_fd[token] + c_gutenberg_fd[token] + ws_suny_fd[token] + ws_gutenberg_fd[token]
    f.write("|{0}|, |{1}|, |{2}|, |{3}|, |{4}|, |{5}|\n".format(token, c_suny_fd[token], c_gutenberg_fd[token], ws_suny_fd[token], ws_gutenberg_fd[token], total))
f.close()
print("Wrote file “{0}” to the disk.".format(filename))
