import os
from dotenv import dotenv_values
from openai import AzureOpenAI
from pydub import AudioSegment, silence


class Transcriber:
    def __init__(self, api_key: str = None, endpoint: str = None, deployment_id: str = "whisper"):
        self.api_key = dotenv_values().get("api_key", api_key) or os.getenv("api_key")
        self.endpoint = dotenv_values().get("endpoint", endpoint) or os.getenv("endpoint")

        print(f"Using endpoint: {self.endpoint}")
        print(f"Using api_key: {self.api_key}")

        self.deployment_id = deployment_id
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-05-01-preview",
        )

    def split_audio_on_silence(self, audio_file_path):
        """
        Split audio based on silence detection.
        """
        audio = AudioSegment.from_file(audio_file_path)

        chunks = silence.split_on_silence(
            audio,
            min_silence_len=1000,  # Silence longer than 1 second
            silence_thresh=audio.dBFS - 14,  # Threshold relative to audio loudness
            keep_silence=500  # Keep small silence padding
        )

        print(f"Audio split into {len(chunks)} logical chunks based on silence.")
        return chunks

    def transcribe_audio_whisper(self, audio_file_path: str) -> str:
        if not os.path.exists(audio_file_path):
            print(f"Audio file not found: {audio_file_path}")
            return None

        chunks = self.split_audio_on_silence(audio_file_path)
        full_transcription = ""

        for idx, chunk in enumerate(chunks):
            chunk_path = f"temp_chunk_{idx}.wav"
            chunk.export(chunk_path, format="wav")

            print(f"Transcribing chunk {idx + 1}/{len(chunks)}...")

            # Corrected: Use 'with' to auto-close the file
            with open(chunk_path, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model=self.deployment_id,
                    file=audio_file,
                )

            transcribed_text = result.text
            full_transcription += f"\n[Part {idx + 1}]\n{transcribed_text}\n"

            os.remove(chunk_path)

        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(full_transcription)

        print("Full transcription saved to transcription.txt")

        return full_transcription


if __name__ == "__main__":
    transcriber = Transcriber()
    transcription = transcriber.transcribe_audio_whisper("output_5_minutes.mp3")
    print(transcription)
