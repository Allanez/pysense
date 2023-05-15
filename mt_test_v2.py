import sounddevice as sd
import numpy as np
import datetime
import wave

def save_wav(filename, data, sample_rate):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data.tobytes())

def record_microphones(duration, sample_rate):
    channels = [1, 2]
    frames_per_buffer = int(sample_rate * duration)

    audio_data = {channel: np.zeros((frames_per_buffer,)) for channel in channels}

    def callback(indata, frames, time, status):
        for channel in channels:
            audio_data[channel] = np.concatenate((audio_data[channel], indata[:, channel - 1]))

    print("Recording started...")
    with sd.InputStream(channels=2, callback=callback, samplerate=sample_rate):
        sd.sleep(int(duration * 1000))

    for channel in channels:
        filename = f"microphone_{channel}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        save_wav(filename, audio_data[channel], sample_rate)
        print(f"Saved audio from microphone {channel} to {filename}")

    print("Recording finished")

record_duration = 5
sample_rate = 44100

record_microphones(record_duration, sample_rate)
