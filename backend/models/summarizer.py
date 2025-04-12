from transformers import pipeline
import os  # Import os for potential environment variable usage
from abc import ABC


class Summarizer(ABC):
    """Abstract base class for summarization models."""

    def __init__(self):
        if os.getenv("PRINT_VERBOSE")=="True":
            self.verbose = True
        else:
            self.verbose = False

    def generate_summary(self, text_to_summarize):
        raise NotImplementedError("Subclasses should implement this method.")


class HuggingFaceSummarizer(Summarizer):
    def __init__(self, model_name="facebook/bart-large-cnn", device=-1):
        """Initializes the Hugging Face summarization pipeline."""
        super().__init__()
        try:
            self.summarizer = pipeline("summarization", model=model_name, device=device)
            if self.verbose:
                print(
                    f"Summarization pipeline loaded successfully with model '{model_name}'."
                )
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            if self.verbose:
                print(
                    "Make sure you have 'transformers' and 'torch' (or 'tensorflow') installed."
                )
            raise

    def generate_summary(self, text_to_summarize):
        """Generates a summary for the given text using the loaded pipeline."""
        print("\n--- Text Sent to Summarization Model ---")
        print(text_to_summarize)
        print("-" * 40)
        print("Generating summary...")
        try:
            summary_result = self.summarizer(
                text_to_summarize, max_length=150, min_length=40, do_sample=False
            )[0]
            final_summary = summary_result["summary_text"]
            return final_summary
        except Exception as e:
            if self.verbose:
                print(f"Error during summarization: {e}")
            return None


# --- Example Usage ---
if __name__ == "__main__":
    pass