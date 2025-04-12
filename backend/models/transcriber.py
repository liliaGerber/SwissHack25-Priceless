import requests
import os
from dotenv import dotenv_values
from openai import AzureOpenAI

class Transcriber:
    def __init__(self, api_key: str= None, endpoint: str = None, deployment_id: str = "whisper"):
        self.api_key = dotenv_values().get("AZURE_OPENAI_API_KEY", api_key)
        if not self.api_key:
            self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = dotenv_values().get("AZURE_OPENAI_ENDPOINT", endpoint)
        if not self.endpoint:
            self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", endpoint)
        print(f"Using endpoint: {self.endpoint}")
        print(f"Using api_key: {self.api_key}")
        self.deployment_id = deployment_id
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-05-01-preview",
        )
        
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
        if not os.path.exists(audio_file_path):
            print(f"Audio file not found: {audio_file_path}")
            return None
        print(f"Audio file found: {audio_file_path}. Transcribing...")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model=self.deployment_id,
                    file=audio_file,
                )
            
            transcribed_text = result.text
            print(f"Transcription successful.")
            
            with open("transcription.txt", "w") as f:
                f.write(transcribed_text + "\n")
            
            # Return the transcribed text
            return transcribed_text
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None
    
if __name__ == "__main__":

    transcriber = Transcriber()
    transcription = transcriber.transcribe_audio_whisper("data_audio/audio_big.mp3")
    print(transcription)