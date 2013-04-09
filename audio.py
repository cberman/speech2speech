import pyaudio
import wave

def getDeviceIndexByName(name):
    global audio
    try: audio
    except: 
        audio = pyaudio.PyAudio()
    num = audio.get_device_count()
    devices = [audio.get_device_info_by_index(i) for i in range(num)]
    devices = map(lambda device: device['name'], devices)
    return devices.index(name)

def play(fn):
    try:
        wf = wave.open(fn, 'rb')
    except IOError:
        return
    outstream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)
    while data:
        outstream.write(data)
        data = wf.readframes(chunk)
    outsream.close()

def saveToFile(data, fn):
    wf = wave.open(fn, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(data)
    wf.close()

def initAudio(index):
    global audio, chunk, stream
    audio = pyaudio.PyAudio()
    chunk = 1024
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
            input=True, frames_per_buffer=chunk, input_device_index=index)

def restream():
    global stream
    try:
        stream.close()
    except: pass
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100,
            input=True, frames_per_buffer=chunk, input_device_index=index)

def getChunk():
    return stream.read(chunk)

def terminate():
    try:
        audio.terminate()
    except: pass
    try:
        stream.close()
    except: pass
