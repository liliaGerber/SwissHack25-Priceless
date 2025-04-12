import textwrap
from database import connect_db
from models.summarizer import HuggingFaceSummarizer

class ClientSummarizer:
    """Handles fetching client data from MongoDB and generating financial summaries."""

    def __init__(
        self,
        summarizer_type="HuggingFace",
        mongo_url="mongodb://localhost:27017/",
        db_name="raiffeisen_enhanced",
    ):
        """ Initializes the summarizer pipeline and MongoDB connection details."""
        if summarizer_type == "HuggingFace":
            self.summarizer = HuggingFaceSummarizer()
        elif summarizer_type == "API_call":
            pass
        else:
            raise ValueError(f"Unknown summarizer type: {summarizer_type}")
        self.mongo_url = mongo_url
        self.db_name = db_name
        self._db = connect_db(mongo_url, db_name)  # Initialize db connection placeholder

    def _fetch_client_data(self, client_name_to_find):
        """Fetches client details and previous discussions from MongoDB."""
        if self._db is None:
            return None, None, None  # Return None if DB connection failed

        customers_collection = self._db["customers"]
        
        # Find the client by name (adjust "name" field if different in your schema)
        customer_data = customers_collection.find_one({"name": client_name_to_find})

        if not customer_data:
            print(f"Client '{client_name_to_find}' not found in database.")
            return None, None, None

        client_id = customer_data.get("_id")
        client_name = customer_data.get("name")
        client_job = customer_data.get("job", "N/A")  # Get job, default if missing

        discussion_docs = list(
            customer_data.get("summaries", [])
        )  
        previous_discussions = discussion_docs

        print(
            f"Found client '{client_name}' ({client_job}) with {len(previous_discussions)} discussions in DB."
        )
        return client_name, client_job, previous_discussions

    def _prepare_text(self, previous_discussions):
        """Formats the input text for the summarization model."""
        if not previous_discussions:
            discussion_points = "- No previous discussions found."
        else:
            discussion_points = " ".join(
                [note["note"] for note in previous_discussions]
            )
        text_to_summarize = discussion_points
        return text_to_summarize

    def generate_summary(
        self, text_to_summarize
    ):
        """Generates a summary for the given text using the loaded pipeline."""
        summary_result = self.summarizer.generate_summary(
            text_to_summarize=text_to_summarize)
        return summary_result

    def summarize_client_from_data(self, previous_discussions):
        """Generates a summary based on provided client data."""
        text = self._prepare_text(previous_discussions)
        summary = self.generate_summary(text)
        return summary

    def summarize_client_from_db(self, client_name_to_find):
        """Fetches client data from the database and generates a summary."""
        client_name, client_job, previous_discussions = self._fetch_client_data(
            client_name_to_find
        )
        if client_name is None:
            return None  

        return self.summarize_client_from_data(
            previous_discussions
        )


if __name__ == "__main__":
    summarizer_instance = ClientSummarizer()  # Use default model and DB settings
    client_name_in_db = summarizer_instance._db["customers"].find_one(
        {}, {"name": 1}
    )["name"]  # Fetch a random client name from the DB

    summary = summarizer_instance.summarize_client_from_db(client_name_in_db)

    if summary:
        print(f"\n--- Generated Client Summary ({client_name_in_db} from DB) ---")
        print(textwrap.fill(summary, width=80))
        print("-" * 40)
    else:
        print(
            f"Failed to generate summary for '{client_name_in_db}' from DB (maybe client not found?)."
        )
