import os
import wave
import time
import numpy as np
import RPi.GPIO as GPIO
import sounddevice as sd
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

# Load environment variables
load_dotenv()

# Set your OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# GPIO pin for the button
BUTTON_PIN = 17

# Parameters for recording
SAMPLE_RATE = 44100

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def record_audio():
    print("Recording...")
    audio = []
    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    stream.start()
    try:
        while GPIO.input(BUTTON_PIN) == GPIO.LOW:
            frame, overflowed = stream.read(1024)
            audio.append(frame)
            time.sleep(0.01)  # Sleep to reduce CPU usage
    finally:
        stream.stop()
        stream.close()
        audio = np.concatenate(audio, axis=0)
        audio = np.array(audio, dtype=np.int16)
        print("Recording stopped.")
        return audio

# Save audio to a file
def save_audio(filename, audio):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

# Transcribe audio using OpenAI Whisper
def transcribe_audio(filename):
    audio_file =  open(filename, 'rb')
    response = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
        response_format='text'
    )
    print(response)
    return response

# Generate text response using OpenAI GPT-4
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant. Your answers should be clear and concise. Always get to the point and only give the important details."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Convert text to speech using OpenAI's text-to-speech
def text_to_speech(text, filename):
    response = client.audio.speech.create(
        model="tts-1",
        voice='alloy',
        input=text
    )
    response.stream_to_file(Path(filename))

# Play audio file
def play_audio(filename):
    audio = AudioSegment.from_file(filename)
    play(audio)

def process_audio(audio):
    save_audio('input.wav', audio)
    prompt = transcribe_audio('input.wav')
    print("You said:", prompt)
    response_text = generate_response(prompt)
    print("Assistant:", response_text)
    text_to_speech(response_text, 'response.mp3')
    play_audio('response.mp3')

print("Press the button to start recording...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            audio = record_audio()
            process_audio(audio)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()



