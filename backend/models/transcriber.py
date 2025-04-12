import requests
import os
from dotenv import dotenv_values

class Transcriber:
    def __init__(self, api_key: str= None, endpoint: str = None, deployment_id: str = "whisper"):
        self.api_key = dotenv_values().get("api_key", api_key)
        if not self.api_key:
            self.api_key = os.getenv("api_key")
        self.endpoint = dotenv_values().get("endpoint", endpoint)
        if not self.endpoint:
            self.endpoint = os.getenv("endpoint", endpoint)
        print(f"Using endpoint: {self.endpoint}")
        print(f"Using api_key: {self.api_key}")
        self.deployment_id = deployment_id
        self.url = f"{self.endpoint}openai/deployments/{self.deployment_id}/audio/transcriptions?api-version=2024-02-01"
    def divide_into_components(self, file_to_path: str, total_chunks: int= 1):
        """
        Divides the audio file into components for processing.
        This is a placeholder function. Actual implementation may vary.
        """
        with open(file_to_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            chunk_size = len(audio_data) // total_chunks
            chunks = [audio_data[i:i + chunk_size] for i in range(0, len(audio_data), chunk_size)]
        return chunks
    
    def transcribe_audio_whisper(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file using Azure OpenAI Whisper API.
        """
        headers = {
            "api-key": self.api_key,
        }

        audio_data = self.divide_into_components(audio_file_path)
        if os.path.exists(audio_file_path):
            print(f"Audio file found: {audio_file_path}")
        else:
            print(f"Audio file not found: {audio_file_path}")
            return None
        transcription_results = []
        with open(audio_file_path, 'rb') as f:
            files = {
                'file': (os.path.basename(audio_file_path), f),
                'language': (None, 'en-US'),
                'model': (None, 'whisper-1'),
            }

            response = requests.post(self.url, headers=headers, files=files)
        print("Okayy")
        if response.status_code != 200:
            print(response.text)
            response.raise_for_status()
        with open("transcription.txt", "w") as f:
            for result in transcription_results:
                f.write(result["text"] + "\n")
        return transcription_results
    
if __name__ == "__main__":

    transcriber = Transcriber()
    transcription = transcriber.transcribe_audio_whisper("data_audio/audio_small.mp3")
    print(transcription)