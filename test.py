def save_file(n):
    print("saving recording " + str(n)+"\n")
    wav_output_filename = 'test' + str(n) + '.wav' # name of .wav file
    
    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    if n == 1:
        wavefile.writeframes(b''.join(f1))
    elif n == 2:
        wavefile.writeframes(b''.join(f2))
    wavefile.close()
