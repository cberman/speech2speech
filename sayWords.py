import audio
from os import path
from sys import argv
from util import par

def init(voice='katie'):
    global recordDir
    audio.initAudio()
    recordDir = path.join(path.dirname(__file__), 'recordings')
    recordDir = path.join(recordDir, voice)

def findWord(word):
    word = ''.join([c for c in word.lower() if c.isalpha()])
    for i in range(len(par)):
        p = ''.join([c for c in par[i].lower() if c.isalpha() or c == ' ']).split()
        if word in p:
            return i, p.index(word)
    return -1, -1

def main():
    init()
    if len(argv) > 1:
        words = argv[1:]
    else:
        words = raw_input('gogogo: ').split()
    for word in words:
        location = findWord(word)
        if -1 in location:
            print '%s is not in the text' % word
            audio.terminate()
            exit()
        fn = '%d.%03d.wav' % location
        audio.play(path.join(recordDir, fn))
    audio.terminate()

if __name__ == '__main__': main()
