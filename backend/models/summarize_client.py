from transformers import pipeline
from pymongo import MongoClient
import textwrap
from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Dict, Any, Union


class Summarizer(ABC):
    """Abstract base class for summarization models."""

    @abstractmethod
    def generate_summary(self, text_to_summarize: str) -> Optional[str]:
        """Generate a summary for the given text.
        
        Args:
            text_to_summarize: The text to be summarized.
            
        Returns:
            The generated summary or None if summarization fails.
        """
        pass


class HuggingFaceSummarizer(Summarizer):
    """Summarizer implementation using Hugging Face models."""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn", device: int = -1):
        """Initialize the Hugging Face summarization pipeline.

        Args:
            model_name: The name of the Hugging Face summarization model.
            device: Device for pipeline (-1 for CPU, 0+ for GPU).
        """
        try:
            self.summarizer = pipeline("summarization", model=model_name, device=device)
            print(f"Summarization pipeline loaded successfully with model '{model_name}'.")
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            print("Make sure you have 'transformers' and 'torch' (or 'tensorflow') installed.")
            raise

    def generate_summary(self, text_to_summarize: str, max_length: int = 150, 
                         min_length: int = 40, do_sample: bool = False) -> Optional[str]:
        """Generate a summary for the given text using the loaded pipeline.

        Args:
            text_to_summarize: The text to be summarized.
            max_length: Maximum length of the summary.
            min_length: Minimum length of the summary.
            do_sample: Whether to use sampling.

        Returns:
            The generated summary text or None if an error occurs.
        """
        print("\n--- Text Sent to Summarization Model ---")
        print(text_to_summarize)
        print("-" * 40)
        print("Generating summary...")
        
        try:
            summary_result = self.summarizer(
                text_to_summarize, 
                max_length=max_length, 
                min_length=min_length, 
                do_sample=do_sample
            )[0]
            return summary_result["summary_text"]
        except Exception as e:
            print(f"Error during summarization: {e}")
            return None


class ClientSummarizer:
    """Handles fetching client data from MongoDB and generating financial summaries."""

    def __init__(
        self,
        summarizer_type: str = "HuggingFace",
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name: str = "raiffeisen_enhanced",
    ):
        """Initialize the summarizer pipeline and MongoDB connection details.

        Args:
            summarizer_type: The type of summarizer to use (currently only "HuggingFace" supported).
            mongo_uri: MongoDB connection URI.
            db_name: MongoDB database name.
        """
        # Initialize the appropriate summarizer based on type
        if summarizer_type == "HuggingFace":
            self.summarizer = HuggingFaceSummarizer()
        else:
            raise ValueError(f"Unsupported summarizer type: {summarizer_type}")

        # MongoDB connection settings
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self._db = None

    def _connect_db(self) -> bool:
        """Establish connection to MongoDB if not already connected.
        
        Returns:
            True if connection is successful, False otherwise.
        """
        if self._db is not None:
            return True
            
        try:
            client = MongoClient(self.mongo_uri)
            # The ismaster command is cheap and does not require auth
            client.admin.command("ismaster")
            self._db = client[self.db_name]
            print(f"Connected to MongoDB database '{self.db_name}'.")
            return True
        except Exception as e:
            print(f"Error connecting to MongoDB at {self.mongo_uri}: {e}")
            self._db = None
            return False

    def _fetch_client_data(self, client_name: str) -> Tuple[Optional[str], Optional[str], List[Dict[str, Any]]]:
        """Fetch client details and previous discussions from MongoDB.

        Args:
            client_name: The name of the client to search for.

        Returns:
            A tuple containing (client_name, client_job, previous_discussions) or 
            (None, None, []) if not found or connection fails.
        """
        if not self._connect_db():
            return None, None, []

        customers_collection = self._db["customers"]
        
        # Find the client by name
        customer_data = customers_collection.find_one({"name": client_name})

        if not customer_data:
            print(f"Client '{client_name}' not found in database.")
            return None, None, []

        client_name = customer_data.get("name")
        client_job = customer_data.get("job", "N/A")  # Default if missing
        
        # Get previous discussions
        previous_discussions = customer_data.get("summaries", [])
        
        print(f"Found client '{client_name}' ({client_job}) with {len(previous_discussions)} discussions in DB.")
        return client_name, client_job, previous_discussions

    def _prepare_text(self, client_name: str, client_job: str, previous_discussions: List[Dict[str, Any]]) -> str:
        """Format the input text for the summarization model.
        
        Args:
            client_name: Client's name.
            client_job: Client's job.
            previous_discussions: List of discussion notes.
            
        Returns:
            Formatted text ready for summarization.
        """
        if not previous_discussions:
            discussion_text = "No previous discussions found."
        else:
            # Extract notes from previous discussions
            discussion_text = " ".join([note.get("note", "") for note in previous_discussions])
        
        return discussion_text

    def summarize_client_from_data(self, client_name: str, client_job: str, 
                                  previous_discussions: List[Dict[str, Any]]) -> Optional[str]:
        """Generate a summary based on provided client data.

        Args:
            client_name: Client's name.
            client_job: Client's job.
            previous_discussions: List of dictionaries, each representing a discussion note.

        Returns:
            The generated summary text, or None if an error occurs.
        """
        text = self._prepare_text(client_name, client_job, previous_discussions)
        return self.summarizer.generate_summary(text)

    def summarize_client_from_db(self, client_name: str) -> Optional[str]:
        """Fetch client data from the database and generate a summary.

        Args:
            client_name: The name of the client to fetch and summarize.

        Returns:
            The generated summary text, or None if client not found or error occurs.
        """
        client_name, client_job, previous_discussions = self._fetch_client_data(client_name)
        
        if client_name is None:
            return None

        return self.summarize_client_from_data(client_name, client_job, previous_discussions)


# Example usage
if __name__ == "__main__":
    summarizer = ClientSummarizer()
    client_name = "Ryan Zimmermann"
    
    summary = summarizer.summarize_client_from_db(client_name)
    
    if summary:
        print(f"\n--- Generated Client Summary for {client_name} ---")
        print(textwrap.fill(summary, width=80))
        print("-" * 40)
    else:
        print(f"Failed to generate summary for '{client_name}' from DB.")