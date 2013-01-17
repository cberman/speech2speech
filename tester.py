import pyaudio, wave
import cmath
from array import array
from math import pi
from struct import unpack
from time import sleep

if __name__ != '__main__': raise ImportError("tester.py is designed to be run in interactive mode, not imported")

pa = pyaudio.PyAudio()
stream = None

def restream():
    global stream
    if stream:
        stream.close()
    stream = pa.open(format=pa.get_format_from_width(cw.getsampwidth()),
            channels=cw.getnchannels(),
            rate=cw.getframerate(), output=True)

def dft(seq):
    def dftk(seq, k):
        N = len(seq)
        total = 0
        for n in range(N):
            total += seq[n] * cmath.exp(-2j*pi * n * k/N)
        return total
    return [dftk(seq, k) for k in range(len(seq))]

def fft(seq):
    N = len(seq)
    if N == 1:
        return [seq[0],]
    else:
        first = fft([seq[i] for i in range(0, N,2)])
        second = fft([seq[i] for i in range(N) if i % 2])
        for k in range(N/2):
            t = first[k]
            first[k] = t + cmath.exp(-2j*pi * k/N) * second[k]
            second[k] = t - cmath.exp(-2j*pi * k/N) * second[k]
        return first + second

cw = wave.open('recordings/collin/0.010.wav', 'rb')
collin = list()
cL = list()
data = cw.readframes(1024)
while data:
    collin.append(data)
    cL.append(unpack('<' + ('h'*(len(data) / 2)), data))
    cL[-1] = array('h', cL[-1])
    data = cw.readframes(1024)
cfft = [fft(L) for L in cL]
cMaxes = [max(map(abs, c)) for c in cfft]
cMaxi = map(lambda a: a if a < 512 else 1023 - a, [map(abs, c).index(max(map(abs, c))) for c in cfft])

kw = wave.open('recordings/katie/0.010.wav', 'rb')
katie = list()
kL = list()
data = kw.readframes(1024)
while data:
    katie.append(data)
    kL.append(unpack('<' + ('h'*(len(data) / 2)), data))
    kL[-1] = array('h', kL[-1])
    data = kw.readframes(1024)
kfft = [fft(L) for L in kL]
kMaxes = [max(map(abs, k)) for k in kfft]
kMaxi = map(lambda a: a if a < 512 else 1023 - a, [map(abs, k).index(max(map(abs, k))) for k in kfft])

def repeat(person=collin, times=5, indicies=None, delay=.1, inbetween=.5):
    indicies = indicies or range(len(person))
    for i in indicies:
        print i
        for t in range(times):
            stream.write(person[i])
            sleep(delay)
            restream()
        sleep(inbetween)

restream()
