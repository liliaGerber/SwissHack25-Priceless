import os
import queue
import numpy as np
import sounddevice as sd
from dotenv import dotenv_values
from pydub import AudioSegment
from openai import AzureOpenAI


class AzureClient:
    def __init__(self, api_key=None, endpoint=None, deployment_id="whisper"):
        config = dotenv_values()
        self.api_key = api_key or config.get("api_key") or os.getenv("api_key")
        self.endpoint = endpoint or config.get("endpoint") or os.getenv("endpoint")
        self.deployment_id = deployment_id

        print(f"Using endpoint: {self.endpoint}")

        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-05-01-preview",
        )

    def transcribe_audio(self, file_path: str) -> str:
        with open(file_path, "rb") as audio_file:
            result = self.client.audio.transcriptions.create(
                model=self.deployment_id,
                file=audio_file,
            )
        return result.text.strip()


class AudioRecorder:
    def __init__(self, samplerate=16000, blocksize=1024):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.q = queue.Queue()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def start_stream(self):
        return sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            channels=1,
            dtype="float32",
            callback=self.audio_callback,
        )


class RealTimeTranscriber:
    def __init__(self, azure_client: AzureClient, audio_recorder: AudioRecorder):
        self.azure_client = azure_client
        self.audio_recorder = audio_recorder

    def transcribe_live(self, duration=2, rms_threshold=150):
        print("Start speaking... (Press CTRL+C to stop)")

        with self.audio_recorder.start_stream():
            buffer = np.empty((0, 1), dtype=np.float32)

            try:
                while True:
                    audio_chunk = self.audio_recorder.q.get()
                    buffer = np.concatenate((buffer, audio_chunk))

                    if len(buffer) >= self.audio_recorder.samplerate * duration:
                        temp_filename = "temp_live_audio.wav"

                        audio_data = (buffer * 32767).astype(np.int16)
                        audio_segment = AudioSegment(
                            audio_data.tobytes(),
                            frame_rate=self.audio_recorder.samplerate,
                            sample_width=2,
                            channels=1,
                        )

                        if audio_segment.rms < rms_threshold:
                            print("...silence detected, skipping...\n")
                            buffer = np.empty((0, 1), dtype=np.float32)
                            continue

                        audio_segment.export(temp_filename, format="wav")

                        text = self.azure_client.transcribe_audio(temp_filename)
                        if text:
                            print(f"YOU SAID: {text}\n")

                        os.remove(temp_filename)
                        buffer = np.empty((0, 1), dtype=np.float32)

            except KeyboardInterrupt:
                print("\nStopping transcription...")


if __name__ == "__main__":
    azure_client = AzureClient()
    audio_recorder = AudioRecorder()
    transcriber = RealTimeTranscriber(azure_client, audio_recorder)
    transcriber.transcribe_live()
