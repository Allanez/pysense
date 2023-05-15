import pyaudio
import wave
import threading
#import multiprocessing
from ctypes import *
from contextlib import contextmanager

ERR_HAND = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

FORMAT = pyaudio.paInt16 # 16-bit resolution
CHANNELS = 1 # 1 channel
RATE = 44100 # 44.1kHz sampling rate
CHUNK = 4096 # 2^12 samples for buffer
DUR = 1 # seconds to record

audio = ""

f1=[]
f2=[]
def py_err_handler(filename, line, function, err, fmt):
    pass

c_err_handler = ERR_HAND(py_err_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_err_handler)
    yield
    asound.snd_lib_error_set_handler(None)

# create pyaudio instantiation
    
def rec_audio(n, index):
    print("thread "+str(n)+"\n" )
    with noalsaerr():
        audio = pyaudio.PyAudio()
        
    dev_index = index # device index found by p.get_device_info_by_index(ii)
    wav_output_filename = 'test' + str(n) + '.wav' # name of .wav file
    
    # create pyaudio stream
    stream = audio.open(format = FORMAT,rate = RATE,channels = CHANNELS, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=CHUNK)
    print("recording audio number " + str(n)+"\n")
    #frames = []

    # loop through stream and append audio chunks to frame array

    for ii in range(0,int((RATE/CHUNK)*DUR)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        if n == 1:
            f1.append(data)
        elif n == 2:
            f2.append(data)
        

    print("finished recording an" + str(n)+"\n")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()


def save_file(n):
    # save the audio frames as .wav file
    wav_output_filename = 'test' + str(n) + '.wav' # name of .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    if n == 1:
        wavefile.writeframes(b''.join(f1))
    elif n == 2:
        wavefile.writeframes(b''.join(f2))
    wavefile.close()

if __name__ =="__main__":
    t1 = threading.Thread(target=rec_audio, args=(1,2,))
    t2 = threading.Thread(target=rec_audio, args=(2,3,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("heh")
    save_file(1)
    save_file(2)

    #p = multiprocessing.Process(target=rec_audio, args=(1,2,))
   # p.start()

    #p2 = multiprocessing.Process(target=rec_audio, args=(2,3,))
   # p2.start()

    #p.join()
    #p2.join()
    
    print("End process")
