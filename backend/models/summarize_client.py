from transformers import pipeline
import textwrap

client_name = "Bob The Builder"
client_job = "Construction Manager"
previous_discussions = [
    "2024-01-10: Initial consultation. Discussed Bob's goal of retiring in 15 years. Reviewed current assets (modest savings, small 401k). Concerned about market volatility.",
    "2024-03-22: Follow-up on risk tolerance. Bob prefers a balanced approach. Agreed on a diversified portfolio strategy (60% equity, 40% bonds). Started funding a Roth IRA.",
    "2024-05-15: Reviewed Q1 performance. Discussed increasing 401k contribution from 5% to 8%. Bob asked about college savings options for his child.",
    "2024-06-30: Explored 529 plan options. Bob decided to open a 529 plan and contribute monthly. Confirmed the 401k contribution increase was implemented."
]


discussion_points = "\n".join([f"- {note}" for note in previous_discussions])

text_to_summarize = f"""
Client Name: {client_name}
Client Job: {client_job}

Summary of Previous Financial Advisory Discussions:
{discussion_points}

Generate a concise summary of the key financial topics, goals, and actions discussed with this client across all sessions.
"""

print("--- Text Sent to Summarization Model ---")
print(text_to_summarize)
print("-" * 40)

#  model from Hugging Face.
# 't5-small', 'google/pegasus-xsum' 
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    print("Summarization pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    print("Make sure you have 'transformers' and 'torch' (or 'tensorflow') installed.")
    exit() 

# ---  Summary ---
print("Generating summary...")
try:
    summary_result = summarizer(
        text_to_summarize,
        max_length=150,  # Maximum words/tokens in the summary
        min_length=40,   # Minimum words/tokens in the summary
        do_sample=False  # Set to False for deterministic output
    )[0] 

    final_summary = summary_result['summary_text']

    #   Result 
    print("\n--- Generated Client Summary ---")
    print(textwrap.fill(final_summary, width=80))
    print("-" * 40)

except Exception as e:
    print(f"Error during summarization: {e}")