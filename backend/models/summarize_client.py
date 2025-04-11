from transformers import pipeline
from pymongo import MongoClient
import textwrap
import os # Import os for potential environment variable usage

class ClientSummarizer:
    """
    Handles fetching client data from MongoDB and generating financial summaries.
    """
    def __init__(self, model_name="facebook/bart-large-cnn", device=-1, mongo_uri="mongodb://localhost:27017/", db_name="raiffeisen"):
        """
        Initializes the summarizer pipeline and MongoDB connection details.

        Args:
            model_name (str): The name of the Hugging Face summarization model.
            device (int): Device for pipeline (-1 for CPU, 0+ for GPU).
            mongo_uri (str): MongoDB connection URI.
            db_name (str): MongoDB database name.
        """
        try:
            self.summarizer = pipeline("summarization", model=model_name, device=device)
            print(f"Summarization pipeline loaded successfully with model '{model_name}'.")
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            print("Make sure you have 'transformers' and 'torch' (or 'tensorflow') installed.")
            raise  # Re-raise the exception to indicate failure

        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self._db = None # Initialize db connection placeholder

    def _connect_db(self):
        """Establishes connection to MongoDB if not already connected."""
        if self._db is None:
            try:
                client = MongoClient(self.mongo_uri)
                # The ismaster command is cheap and does not require auth.
                client.admin.command('ismaster')
                self._db = client[self.db_name]
                print(f"Connected to MongoDB database '{self.db_name}'.")
            except Exception as e:
                print(f"Error connecting to MongoDB at {self.mongo_uri}: {e}")
                self._db = None # Ensure db is None if connection fails
                raise # Re-raise connection error

    def _fetch_client_data(self, client_name_to_find):
        """
        Fetches client details and previous discussions from MongoDB.

        Args:
            client_name_to_find (str): The name of the client to search for.

        Returns:
            tuple: (client_name, client_job, previous_discussions) or (None, None, None) if not found.
        """
        self._connect_db() # Ensure DB connection
        if not self._db:
            return None, None, None # Return None if DB connection failed

        customers_collection = self._db["customers"]
        summaries_collection = self._db["summaries"] # Assuming discussions are here

        # Find the client by name (adjust "name" field if different in your schema)
        customer_data = customers_collection.find_one({"name": client_name_to_find})

        if not customer_data:
            print(f"Client '{client_name_to_find}' not found in database.")
            return None, None, None

        client_id = customer_data.get("_id")
        client_name = customer_data.get("name")
        client_job = customer_data.get("job", "N/A") # Get job, default if missing

        # Find previous discussions linked by client_id (adjust "client_id" field if different)
        # Also assume discussions are stored in a field named "summary" within the summaries collection
        discussion_docs = list(summaries_collection.find({"client_id": client_id}).sort("date", 1)) # Sort by date ascending
        previous_discussions = [doc.get("summary", "Summary not available") for doc in discussion_docs]

        print(f"Found client '{client_name}' ({client_job}) with {len(previous_discussions)} discussions in DB.")
        return client_name, client_job, previous_discussions

    def _prepare_text(self, client_name, client_job, previous_discussions):
        """Formats the input text for the summarization model."""
        if not previous_discussions:
             discussion_points = "- No previous discussions found."
        else:
            discussion_points = "\n".join([f"- {note}" for note in previous_discussions])

        text_to_summarize = f"""
Client Name: {client_name}
Client Job: {client_job}

Summary of Previous Financial Advisory Discussions:
{discussion_points}

Generate a concise summary of the key financial topics, goals, and actions discussed with this client across all sessions. Focus on financial goals, strategies implemented, and outstanding items.
"""
        return text_to_summarize

    def generate_summary(self, text_to_summarize, max_length=150, min_length=40, do_sample=False):
        """
        Generates a summary for the given text using the loaded pipeline.

        Args:
            text_to_summarize (str): The text to be summarized.
            max_length (int): Maximum length of the summary.
            min_length (int): Minimum length of the summary.
            do_sample (bool): Whether to use sampling.

        Returns:
            str: The generated summary text, or None if an error occurs.
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
            final_summary = summary_result['summary_text']
            return final_summary
        except Exception as e:
            print(f"Error during summarization: {e}")
            return None

    def summarize_client_from_data(self, client_name, client_job, previous_discussions):
        """
        Generates a summary based on provided client data.

        Args:
            client_name (str): Client's name.
            client_job (str): Client's job.
            previous_discussions (list): List of strings, each representing a discussion note.

        Returns:
            str: The generated summary text, or None if an error occurs.
        """
        text = self._prepare_text(client_name, client_job, previous_discussions)
        summary = self.generate_summary(text)
        return summary

    def summarize_client_from_db(self, client_name_to_find):
        """
        Fetches client data from the database and generates a summary.

        Args:
            client_name_to_find (str): The name of the client to fetch and summarize.

        Returns:
            str: The generated summary text, or None if client not found or error occurs.
        """
        client_name, client_job, previous_discussions = self._fetch_client_data(client_name_to_find)

        if client_name is None:
            return None # Client not found or DB error

        return self.summarize_client_from_data(client_name, client_job, previous_discussions)

# --- Example Usage ---
if __name__ == "__main__":
    # --- Option 1: Summarize hardcoded data (like original script) ---
    print("--- Example 1: Summarizing Hardcoded Data ---")
    hardcoded_client_name = "Bob The Builder"
    hardcoded_client_job = "Construction Manager"
    hardcoded_discussions = [
        "2024-01-10: Initial consultation. Discussed Bob's goal of retiring in 15 years. Reviewed current assets (modest savings, small 401k). Concerned about market volatility.",
        "2024-03-22: Follow-up on risk tolerance. Bob prefers a balanced approach. Agreed on a diversified portfolio strategy (60% equity, 40% bonds). Started funding a Roth IRA.",
        "2024-05-15: Reviewed Q1 performance. Discussed increasing 401k contribution from 5% to 8%. Bob asked about college savings options for his child.",
        "2024-06-30: Explored 529 plan options. Bob decided to open a 529 plan and contribute monthly. Confirmed the 401k contribution increase was implemented."
    ]

    try:
        summarizer_instance = ClientSummarizer() # Use default model and DB settings
        summary1 = summarizer_instance.summarize_client_from_data(
            hardcoded_client_name, hardcoded_client_job, hardcoded_discussions
        )

        if summary1:
            print("\n--- Generated Client Summary (Hardcoded Data) ---")
            print(textwrap.fill(summary1, width=80))
            print("-" * 40)
        else:
            print("Failed to generate summary for hardcoded data.")

    except Exception as e:
         print(f"Error initializing or using summarizer for hardcoded data: {e}")


    # --- Option 2: Summarize data fetched from MongoDB ---
    print("\n\n--- Example 2: Summarizing Data from MongoDB ---")
    # !! IMPORTANT !!: Replace "Alice Wonderland" with a client name ACTUALLY IN YOUR DATABASE
    client_name_in_db = "Alice Johnson" # <--- CHANGE THIS to a name in your 'customers' collection

    try:
        # Re-use the instance or create a new one if needed
        # summarizer_instance = ClientSummarizer()
        summary2 = summarizer_instance.summarize_client_from_db(client_name_in_db)

        if summary2:
            print(f"\n--- Generated Client Summary ({client_name_in_db} from DB) ---")
            print(textwrap.fill(summary2, width=80))
            print("-" * 40)
        else:
            print(f"Failed to generate summary for '{client_name_in_db}' from DB (maybe client not found?).")

    except Exception as e:
         print(f"Error initializing or using summarizer for DB data: {e}")

    # Close MongoDB client connection if it was opened (optional, depends on app structure)
    # if summarizer_instance._db:
    #     summarizer_instance._db.client.close()
    #     print("MongoDB connection closed.")

# --- Delete the old procedural code ---
# client_name = "Bob The Builder"
# client_job = "Construction Manager"
# previous_discussions = [
#     "2024-01-10: Initial consultation. Discussed Bob's goal of retiring in 15 years. Reviewed current assets (modest savings, small 401k). Concerned about market volatility.",
#     "2024-03-22: Follow-up on risk tolerance. Bob prefers a balanced approach. Agreed on a diversified portfolio strategy (60% equity, 40% bonds). Started funding a Roth IRA.",
#     "2024-05-15: Reviewed Q1 performance. Discussed increasing 401k contribution from 5% to 8%. Bob asked about college savings options for his child.",
#     "2024-06-30: Explored 529 plan options. Bob decided to open a 529 plan and contribute monthly. Confirmed the 401k contribution increase was implemented."
# ]
# 
# 
# discussion_points = "\n".join([f"- {note}" for note in previous_discussions])
# 
# text_to_summarize = f"""
# Client Name: {client_name}
# Client Job: {client_job}
# 
# Summary of Previous Financial Advisory Discussions:
# {discussion_points}
# 
# Generate a concise summary of the key financial topics, goals, and actions discussed with this client across all sessions.
# """
# 
# print("--- Text Sent to Summarization Model ---")
# print(text_to_summarize)
# print("-" * 40)
# 
# #  model from Hugging Face.
# # 't5-small', 'google/pegasus-xsum' 
# try:
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
#     print("Summarization pipeline loaded successfully.")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     print("Make sure you have 'transformers' and 'torch' (or 'tensorflow') installed.")
#     exit() 
# 
# # ---  Summary ---
# print("Generating summary...")
# try:
#     summary_result = summarizer(
#         text_to_summarize,
#         max_length=150,  # Maximum words/tokens in the summary
#         min_length=40,   # Minimum words/tokens in the summary
#         do_sample=False  # Set to False for deterministic output
#     )[0] 
# 
#     final_summary = summary_result['summary_text']
# 
#     #   Result 
#     print("\n--- Generated Client Summary ---")
#     print(textwrap.fill(final_summary, width=80))
#     print("-" * 40)
# 
# except Exception as e:
#     print(f"Error during summarization: {e}")