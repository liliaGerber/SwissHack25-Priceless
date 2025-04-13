from models.real_time_transcriber_without_noise import RealTimeTranscriber
from agents.agent_executer import AgentExec

def main():
    # Initialize the real-time transcriber
    transcriber = RealTimeTranscriber()
    
    last_speaker = None
    # Start transcribing
    transcriber.transcribe_live()
    while True:
        # Get the current speaker
        current_speaker = transcriber.current_speaker
        if last_speaker != current_speaker:
            print(f"Speaker {current_speaker} is speaking.")
            last_speaker = current_speaker

        # Process the audio data
        audio_data = transcriber.q.get()
        if audio_data is not None:
            # Here you can add your processing logic
            pass