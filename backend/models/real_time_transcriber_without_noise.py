import os
import time
import queue
import sounddevice as sd
import numpy as np
from dotenv import dotenv_values
from openai import AzureOpenAI
from pydub import AudioSegment
import librosa  # Add librosa import


class RealTimeTranscriber:
    def __init__(self, api_key=None, endpoint=None, deployment_id="whisper"):
        config = dotenv_values()
        self.api_key = api_key or config.get("api_key") or os.getenv("api_key")
        self.endpoint = endpoint or config.get("endpoint") or os.getenv("endpoint")

        print(f"Using endpoint: {self.endpoint}")

        self.deployment_id = deployment_id
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-05-01-preview",
        )

        self.q = queue.Queue()
        self.max_speakers = 2
        self.speaker_profiles = {1: [], 2: []}
        self.current_speaker = 1  
        self.pitch_threshold = 30

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Put raw float32 data into the queue
        self.q.put(indata.copy())

    def get_pitch(self, audio_data, samplerate):
        """Extracts the median pitch from an audio chunk using librosa.pyin."""
        try:
            # Ensure audio_data is float and mono
            if audio_data.dtype != np.float32:
                 audio_data = audio_data.astype(np.float32)
                 # Normalize if it was int16 previously, check range first if needed
                 if np.max(np.abs(audio_data)) > 1.0:
                     audio_data = audio_data / 32767.0

            if audio_data.ndim > 1:
                audio_data = audio_data.flatten() # Make it 1D, assuming mono input stream

            f0, voiced_flag, voiced_probs = librosa.pyin(audio_data,
                                                         fmin=librosa.note_to_hz('C2'),
                                                         fmax=librosa.note_to_hz('C7'),
                                                         sr=samplerate)
            # Get pitch only for voiced segments
            voiced_f0 = f0[voiced_flag]
            if len(voiced_f0) > 0:
                return np.median(voiced_f0) # Use median pitch of voiced segments
        except Exception as e:
            print(f"Error calculating pitch: {e}")
        return None # No voiced segments detected or error occurred

    def identify_speaker(self, current_pitch):
        """Identifies speaker (1 or 2) based on pitch history."""
        if current_pitch is None:
             return self.current_speaker # Keep current speaker if no pitch

        # --- Initial Speaker Assignment --- 
        if not self.speaker_profiles[1]:
            self.speaker_profiles[1].append(current_pitch)
            self.current_speaker = 1
            print(f"*** Assigning first pitch {current_pitch:.2f} Hz to Speaker 1 ***")
            return self.current_speaker

        # If Speaker 2 has no profile yet
        if not self.speaker_profiles[2]:
            mean_pitch_sp1 = np.mean(self.speaker_profiles[1])
            # If current pitch is different enough from Speaker 1, assign to Speaker 2
            if abs(current_pitch - mean_pitch_sp1) > self.pitch_threshold:
                self.speaker_profiles[2].append(current_pitch)
                self.current_speaker = 2
                print(f"*** Assigning new pitch {current_pitch:.2f} Hz to Speaker 2 (distinct from Sp1 mean {mean_pitch_sp1:.2f} Hz) ***")
            else:
                # Otherwise, still Speaker 1
                self.speaker_profiles[1].append(current_pitch)
                self.current_speaker = 1
                # print(f"Assigning pitch {current_pitch:.2f} Hz to Speaker 1 (similar to mean {mean_pitch_sp1:.2f} Hz)")
            return self.current_speaker

        # --- Both speakers have profiles, find the closest match --- 
        mean_pitch_sp1 = np.mean(self.speaker_profiles[1])
        mean_pitch_sp2 = np.mean(self.speaker_profiles[2])

        diff1 = abs(current_pitch - mean_pitch_sp1)
        diff2 = abs(current_pitch - mean_pitch_sp2)

        if diff1 <= diff2:
            # Closer to Speaker 1
            self.current_speaker = 1
            self.speaker_profiles[1].append(current_pitch)
        else:
            # Closer to Speaker 2
            self.current_speaker = 2
            self.speaker_profiles[2].append(current_pitch)
            # Optional: Limit profile history size
            # if len(self.speaker_profiles[2]) > 20: self.speaker_profiles[2].pop(0)

        # print(f"Pitch {current_pitch:.2f} Hz -> Speaker {self.current_speaker} (Means: Sp1={mean_pitch_sp1:.2f}, Sp2={mean_pitch_sp2:.2f})")
        return self.current_speaker

    def transcribe_live(self):
        samplerate = 16000
        blocksize = 1024 
        duration = 2  # Process audio every 2 seconds
        rms_threshold = 0.004 # Silence detection threshold for float32 data (-40 dBFS)

        print("Start speaking... (Press CTRL+C to stop)")

        stream = sd.InputStream(
            samplerate=samplerate,
            blocksize=blocksize, # Might consider larger blocksize for less frequent callbacks
            channels=1,
            dtype="float32", # Input stream is float32
            callback=self.audio_callback,
        )

        with stream:
            buffer = np.empty((0, 1), dtype=np.float32)
            live_transcription = ""

            try:
                while True:
                    audio_chunk = self.q.get()
                    buffer = np.concatenate((buffer, audio_chunk))

                    if len(buffer) >= samplerate * duration:
                        current_buffer_segment = buffer[:samplerate * duration] # Process fixed duration
                        buffer = buffer[samplerate * duration:] # Keep remainder for next chunk

                        # --- Silence Detection ---
                        # Calculate RMS on the float32 data directly
                        rms_val = np.sqrt(np.mean(current_buffer_segment**2))
                        if rms_val < rms_threshold:
                            print(f"...silence detected (RMS: {rms_val:.4f}), skipping...")
                            continue # Skip processing this silent segment

                        # --- Pitch Analysis & Speaker ID ---
                        current_pitch = self.get_pitch(current_buffer_segment, samplerate)
                        speaker_id = self.identify_speaker(current_pitch)
                        pitch_str = f"{current_pitch:.2f} Hz" if current_pitch else "N/A"

                        temp_filename = "temp_live_audio.wav"
                        audio_data_int16 = (current_buffer_segment * 32767).astype(np.int16)
                        audio_segment = AudioSegment(
                            audio_data_int16.tobytes(), frame_rate=samplerate, sample_width=2, channels=1
                        )
                        audio_segment.export(temp_filename, format="wav")

                        # --- Transcription ---
                        try:
                            with open(temp_filename, "rb") as audio_file:
                                result = self.client.audio.transcriptions.create(
                                    model=self.deployment_id,
                                    file=audio_file,
                                    language="en"
                                )
                            text = result.text.strip()
                        except Exception as e:
                            print(f"Error during transcription API call: {e}")
                            text = ""
                        finally:
                             # Ensure temp file is always removed
                             if os.path.exists(temp_filename):
                                 os.remove(temp_filename)


                        if text:
                            speaker_tag = f"[Speaker {speaker_id}]"
                            print(f"{speaker_tag} (Pitch: {pitch_str}): {text}")
                            live_transcription += f"{speaker_tag} {text} "
                        else:
                            # Keep buffer if transcription failed? Or just proceed? Currently proceeds.
                            print(f"[Speaker {speaker_id}] (Pitch: {pitch_str}): --- (Transcription failed or empty) ---")


            except KeyboardInterrupt:
                print("\nStopping transcription...")
                # Optionally save transcript
                # timestamp = time.strftime("%Y%m%d-%H%M%S")
                # filename = f"live_transcription_{timestamp}.txt"
                # with open(filename, "w", encoding="utf-8") as f:
                #     f.write(live_transcription)
                # print(f"Your full transcription is saved in '{filename}'")
            except Exception as e:
                 print(f"\nAn unexpected error occurred: {e}")
            finally:
                # Ensure stream is closed and temp files removed if loop breaks unexpectedly
                if stream and not stream.closed:
                    stream.stop()
                    stream.close()
                    print("Audio stream closed.")
                if os.path.exists("temp_live_audio.wav"):
                    os.remove("temp_live_audio.wav")


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.transcribe_live()
