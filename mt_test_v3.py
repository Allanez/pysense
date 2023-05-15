import pyaudio
import wave
import datetime
import threading
from ctypes import *
from contextlib import contextmanager

ERR_HAND = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_err_handler(filename, line, function, err, fmt):
    pass

c_err_handler = ERR_HAND(py_err_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_err_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def save_wav(filename, frames, sample_width, sample_rate):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(sample_width)  # Sample width in bytes
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)

def record_microphone(stream, frames_per_buffer, channel, duration, sample_width, sample_rate):
    frames = []
    for _ in range(int(duration * sample_rate / frames_per_buffer)):
        data = stream.read(frames_per_buffer)
        frames.append(data)

    filename = f"microphone_{channel}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    save_wav(filename, b''.join(frames), sample_width, sample_rate)
    print(f"Saved audio from microphone {channel} to {filename}")

def record_microphones(duration, sample_rate):
    channels = [2, 3]  # Channels for the two microphones
    sample_width = 2  # 16-bit audio
    frames_per_buffer = int(sample_rate * duration)
    with noalsaerr():
        p = pyaudio.PyAudio()

    streams = []
    for channel in channels:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=sample_rate,
                        input=True,
                        input_device_index=channel,
                        frames_per_buffer=frames_per_buffer)
        streams.append(stream)

    threads = []
    for i, stream in enumerate(streams):
        thread = threading.Thread(target=record_microphone,
                                  args=(stream, frames_per_buffer, channels[i], duration, sample_width, sample_rate))
        threads.append(thread)
        thread.start()

    print("Recording started...")
    for thread in threads:
        thread.join()

    for stream in streams:
        stream.stop_stream()
        stream.close()

    p.terminate()
    print("Recording finished.")

# Example usage
record_duration = 5  # Recording duration in seconds
sample_rate = 44100  # Sample rate in Hz

record_microphones(record_duration, sample_rate)
