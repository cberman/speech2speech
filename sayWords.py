from util import par

def findWord(word):
    word = ''.join([c for c in word.lower() if c.isalpha()])
    for i in range(len(par)):
        p = ''.join([c for c in par[i].lower() if c.isalpha() or c == ' ']).split()
        if word in p:
            return i, p.index(word)

print '%d.%03d.wav' % findWord('goat')
