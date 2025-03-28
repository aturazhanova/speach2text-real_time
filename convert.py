import queue
import sounddevice as sd
import vosk
import json

# Set up the audio input parameters
SAMPLE_RATE = 16000
BUFFER_DURATION = 2  # seconds of buffer

# Load the Vosk model (download a model first from https://alphacephei.com/vosk/models)
model_path = "/Users/aigerim/Desktop/Books/speach/model"
model = vosk.Model(model_path)

# Create a queue to hold audio data
audio_queue = queue.Queue()

# Callback function to feed audio data into the queue
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

# Open an audio stream using sounddevice
with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Listening...")

    rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    while True:
        data = audio_queue.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print(result.get("text", ""))
        else:
            partial_result = json.loads(rec.PartialResult())
            print(partial_result.get("partial", ""), end="\r")
