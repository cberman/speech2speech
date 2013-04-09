import getopt
import os
import audio
import wave
from array import array
from collections import defaultdict
from struct import unpack
from sys import argv, exit
from time import sleep
from Tkinter import BOTH, Canvas, Tk, YES
from util import par

def init():
    global w, p, root, canvas, indicies, stream, recordDir, micName
    w = 0
    p = 0
    root, canvas = setUpCanvas()
    indicies = [[4 for i in range(len(par[j].split())+1)] 
            for j in range(len(par))]
    for j in range(0, len(indicies)):
        for i in range(1, len(indicies[j])):
            indicies[j][i] = indicies[j][i-1] + \
                    len(par[j].split()[i-1]) + 1
    recordDir = os.path.join(os.path.dirname(__file__), 'recordings')
    micName = '/dev/dsp2'

def setUpCanvas():
    root = Tk()
    root.title("Comma Gets a Cure")
    canvas = Canvas(root, width=640, height=480, bg='white')
    canvas.pack(expand=YES, fill=BOTH)
    root.bind('<Right>', highlight)
    root.bind('<q>', quit)
    root.bind('<Left>', dehighlight)
    root.bind('<space>', play)
    root.bind('<d>', delete)
    root.bind('<Down>', lambda evt: [highlight(None) for i in range(5)])
    root.bind('<Up>', lambda evt: [dehighlight(None) for i in range(5)])
    return root, canvas

def highlight(evt):
    global w, p
    font = 'Courier'
    canvas.delete('all')
    canvas.create_text(325, 240, width=630, 
            text=par[p][:indicies[p][w]]+unichr(160)*(len(par[p].split()[w]))+' '+par[p][indicies[p][w+1]:],
            fill='black', font=(font, '18', 'bold'))
    only = '    '
    for i in range(len(par[p].split())):
        if i == w:
            only += par[p].split()[w]
        else:
            only += unichr(160)*len(par[p].split()[i])
        only += ' '
    try:
        fn = os.path.join(recordDir, '%d.%03d.wav' % (p, w))
        #print fn
        wf = wave.open(fn, 'rb')
        color = 'green'
    except:
        color = 'red'
    canvas.create_text(325, 240, width=630, text=only, 
            fill=color, font=(font, '18', 'bold'))
    w += 1
    if w > len(indicies[p])-2:
        w = 0
        p = min(len(par)-1, p+1)
    elif par[p].split()[w] == '-': w += 1    # hypens are not words

def dehighlight(evt):
    global w, p
    w -= 1
    if w < 1:
        if p > 0:
            p -= 1
            w = len(indicies[p])-2
        else:
            w = 1
    elif par[p].split()[w] == '-': w -= 1    # hypens are not words
    font = 'Courier'
    canvas.delete('all')
    canvas.create_text(325, 240, width=630, 
            text=par[p][:indicies[p][w-1]]+unichr(160)*(len(par[p].split()[w-1]))+' '+par[p][indicies[p][w]:], 
            fill='black', font=(font, '18', 'bold'))
    only = '    '
    for i in range(len(par[p].split())):
        if i == w-1:
            only += par[p].split()[w-1]
        else:
            only += unichr(160)*len(par[p].split()[i])
        only += ' '
    try:
        fn = os.path.join(recordDir, '%d.%03d.wav' % (p, w - 1))
        #print fn
        wf = wave.open(fn, 'rb')
        color = 'green'
    except:
        color = 'red'
    canvas.create_text(325, 240, width=630, text=only, 
            fill=color, font=(font, '18', 'bold'))

def play(evt):
    fn = os.path.join(recordDir, '%d.%03d.wav' % (p, w - 1))
    audio.play(fn)

def delete(evt):
    fn = os.path.join(recordDir, '%d.%03d.wav' % (p, w - 1))
    try:
        wf = wave.open(fn, 'rb')
        wf.close()
        os.remove(fn)
        dehighlight(None)
        highlight(None)
    except IOError:
        return

def quit(evt):
    audio.terminate()
    exit()

def usage():
    pass

def parseArgs():
    global recordDir, micName
    options = 'r:m:'
    long_options = ['record-dir=', 'mic-name=']
    try:
        optlist, args = getopt.getopt(argv[1:], options, long_options)
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt, arg in optlist:
        if opt in ('-r', '--record-dir'):
            recordDir = os.path.join(recordDir, arg)
            if not os.path.exists(recordDir):
                os.makedirs(recordDir)
        elif opt in ('-m', '--mic-name'):
            micName = arg
        else:
            assert False, 'unhandled option'

def main():
    init()
    parseArgs()
    audio.initAudio(audio.getDeviceIndexByName(micName))
    highlight(None) # jump to first word
    threshold = 900
    recording = 0
    while True:
        canvas.update()
        try:
            data = audio.getChunk()
        except IOError:
            quit(None)
        L = unpack('<' + ('h'*(len(data) / 2)), data)
        L = array('h', L)
        # print max(L)
        if max(L) > threshold:
            if not recording:
                recording = 40
                all = list()
            all.append(data)
        elif recording:
            recording -= 1
            if not recording:
                fn = os.path.join(recordDir, '%d.%03d.wav' % (p, w-1))
                if os.path.exists(fn):
                    all = list()
                else:
                    audio.saveToFile(''.join(all), fn)
                    audio.restream()
                    highlight(None)
    root.mainloop()

if __name__ == '__main__': main()
