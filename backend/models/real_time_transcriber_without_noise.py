import os
import time
import queue
import sounddevice as sd
import numpy as np
from dotenv import dotenv_values
from openai import AzureOpenAI
from pydub import AudioSegment


class RealTimeTranscriber:
    def __init__(self, api_key=None, endpoint=None, deployment_id="whisper"):
        config = dotenv_values()
        self.api_key = api_key or config.get("api_key") or os.getenv("api_key")
        self.endpoint = endpoint or config.get("endpoint") or os.getenv("endpoint")

        print(f"Using endpoint: {self.endpoint}")

        self.deployment_id = deployment_id
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-05-01-preview",
        )

        self.q = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def transcribe_live(self):
        samplerate = 16000
        blocksize = 1024
        duration = 2  # Transcribe every 2 seconds
        rms_threshold = 150  # Detect speech if RMS is above this

        print("Start speaking... (Press CTRL+C to stop)")

        stream = sd.InputStream(
            samplerate=samplerate,
            blocksize=blocksize,
            channels=1,
            dtype="float32",
            callback=self.audio_callback,
        )

        with stream:
            buffer = np.empty((0, 1), dtype=np.float32)
            live_transcription = ""

            try:
                while True:
                    audio_chunk = self.q.get()
                    buffer = np.concatenate((buffer, audio_chunk))

                    if len(buffer) >= samplerate * duration:
                        temp_filename = "temp_live_audio.wav"

                        audio_data = (buffer * 32767).astype(np.int16)
                        audio_segment = AudioSegment(
                            audio_data.tobytes(), frame_rate=samplerate, sample_width=2, channels=1
                        )

                        if audio_segment.rms < rms_threshold:
                            print("...silence detected, skipping...\n")
                            buffer = np.empty((0, 1), dtype=np.float32)
                            continue

                        audio_segment.export(temp_filename, format="wav")

                        with open(temp_filename, "rb") as audio_file:
                            result = self.client.audio.transcriptions.create(
                                model=self.deployment_id,
                                file=audio_file,
                            )

                        text = result.text.strip()
                        if text:
                            print(f"YOU SAID: {text}\n")
                            live_transcription += text + " "

                        os.remove(temp_filename)
                        buffer = np.empty((0, 1), dtype=np.float32)

            except KeyboardInterrupt:
                print("\nStopping transcription...")
                # with open("live_transcription.txt", "w", encoding="utf-8") as f:
                #     f.write(live_transcription)
                # print("Your full transcription is saved in 'live_transcription.txt'")


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.transcribe_live()
