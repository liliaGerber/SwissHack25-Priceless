import os
from openai import AzureOpenAI
from dotenv import load_dotenv, dotenv_values

load_dotenv()

DEFAULT_DEPLOYMENT_NAME = "gpt-4o-mini" 
API_VERSION = "2024-02-01" 

class Summarizer:
    def __init__(self, deployment_name: str = None):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY") or dotenv_values().get("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or dotenv_values().get("AZURE_OPENAI_ENDPOINT")
        
        self.deployment_name = deployment_name or \
                               os.getenv("AZURE_OPENAI_DEPLOYMENT_SUMMARIZER") or \
                               DEFAULT_DEPLOYMENT_NAME

        if not self.api_key:
            raise ValueError("Azure OpenAI API key not found. Set AZURE_OPENAI_API_KEY environment variable or in .env file.")
        if not self.endpoint:
            raise ValueError("Azure OpenAI endpoint not found. Set AZURE_OPENAI_ENDPOINT environment variable or in .env file.")

        print(f"Using Azure OpenAI endpoint: {self.endpoint}")
        print(f"Using deployment name for summarization: {self.deployment_name}")

        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=API_VERSION,
        )

    def summarize_text(self, text: str) -> str | None:
        """Summarizes the provided text using the configured Azure OpenAI model."""
        if not text:
            print("Error: Input text is empty.")
            return None
            
        system_prompt = "You are an AI assistant specialized in summarizing meeting transcriptions concisely."
        user_prompt = f"Please provide a brief summary as a whole text without deviding to key points of main points and decisions from the following transcription in language they are talking:\n\n---\n{text}\n---"
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name, 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5, 
                max_tokens=250,
            )
            
            summary = response.choices[0].message.content.strip()
            print("Summary generated successfully.")
            return summary
            
        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            return None

    def summarize_from_file(self, file_path: str) -> str | None:
        """Reads text from a file and summarizes it."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"Reading transcription from: {file_path}")
                transcription_text = f.read()
            
            if not transcription_text.strip():
                print(f"Error: File '{file_path}' is empty.")
                return None
                
            return self.summarize_text(transcription_text)
            
        except FileNotFoundError:
            print(f"Error: Input file not found at {file_path}")
            return None
        except Exception as e:
            print(f"An error occurred reading the file: {e}")
            return None

if __name__ == "__main__":
    # Assumes the script is run from the 'backend' directory
    input_transcription_file = os.path.join("models", "transcription.txt") 
    output_summary_file = os.path.join("models", "summary.txt")

    try:
        summarizer = Summarizer()
        summary = summarizer.summarize_from_file(input_transcription_file)

        if summary:
            print("\n--- Generated Summary ---")
            print(summary)
            
            try:
                with open(output_summary_file, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"\nSummary saved to: {output_summary_file}")
            except Exception as e:
                print(f"Error saving summary to file: {e}")
        else:
            print("Summarization failed.")

    except ValueError as ve: # Catch configuration errors
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")