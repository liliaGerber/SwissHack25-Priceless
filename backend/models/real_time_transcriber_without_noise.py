import os
import time
import queue
import sounddevice as sd
import numpy as np
from dotenv import dotenv_values
from openai import AzureOpenAI
from pydub import AudioSegment
import librosa
import copy

from agents.agent_executer import AgentExec


class RealTimeTranscriber:
    def __init__(self, api_key=None, endpoint=None, deployment_id="whisper"):
        config = dotenv_values()
        self.api_key = api_key or config.get("api_key") or os.getenv("api_key")
        self.endpoint = endpoint or config.get("endpoint") or os.getenv("endpoint")
        self.agent = AgentExec()
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

        self.speaker_segments = {1: [], 2: []}
        self.current_segment_text = ""
        self.silence_duration = 0
        self.silence_threshold_secs = 1.5

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Put raw float32 data into the queue
        self.q.put(indata.copy())

    def initialize_agent_snippet(self):
        self.agent.execute("67f9ebbe72b23bd97cd9ada3", self.current_segment_text)

    def get_pitch(self, audio_data, samplerate):
        try:
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
                if np.max(np.abs(audio_data)) > 1.0:
                    audio_data = audio_data / 32767.0

            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()

            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio_data, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=samplerate
            )

            voiced_f0 = f0[voiced_flag]
            if len(voiced_f0) > 0:
                return np.median(voiced_f0)
        except Exception as e:
            print(f"Error calculating pitch: {e}")
        return None

    def identify_speaker(self, current_pitch):
        if current_pitch is None:
            return self.current_speaker

        if not self.speaker_profiles[1]:
            self.speaker_profiles[1].append(current_pitch)
            self.current_speaker = 1
            return self.current_speaker

        if not self.speaker_profiles[2]:
            mean_pitch_sp1 = np.mean(self.speaker_profiles[1])
            if abs(current_pitch - mean_pitch_sp1) > self.pitch_threshold:
                self.speaker_profiles[2].append(current_pitch)
                self.current_speaker = 2
            else:
                self.speaker_profiles[1].append(current_pitch)
                self.current_speaker = 1
            return self.current_speaker

        mean_pitch_sp1 = np.mean(self.speaker_profiles[1])
        mean_pitch_sp2 = np.mean(self.speaker_profiles[2])

        diff1 = abs(current_pitch - mean_pitch_sp1)
        diff2 = abs(current_pitch - mean_pitch_sp2)

        if diff1 <= diff2:
            self.current_speaker = 1
            self.speaker_profiles[1].append(current_pitch)
        else:
            self.current_speaker = 2
            self.speaker_profiles[2].append(current_pitch)

        return self.current_speaker

    def transcribe_live(self):
        samplerate = 16000
        blocksize = 1024
        duration = 2
        rms_threshold = 0.006

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

            try:
                while True:
                    audio_chunk = self.q.get()
                    buffer = np.concatenate((buffer, audio_chunk))

                    if len(buffer) >= samplerate * duration:
                        current_buffer_segment = buffer[:samplerate * duration]
                        buffer = buffer[samplerate * duration:]

                        rms_val = np.sqrt(np.mean(current_buffer_segment ** 2))

                        if rms_val < rms_threshold:
                            self.silence_duration += duration
                            if self.silence_duration >= self.silence_threshold_secs:
                                if self.current_segment_text.strip():
                                    print(f"=== Speaker {self.current_speaker} Finished ===")
                                    self.speaker_segments[self.current_speaker].append(self.current_segment_text.strip())
                                    self.initialize_agent_snippet()
                                    self.current_segment_text = ""
                                continue
                        else:
                            self.silence_duration = 0

                        current_pitch = self.get_pitch(current_buffer_segment, samplerate)
                        last_speaker_id = copy.deepcopy(self.current_speaker)
                        speaker_id = self.identify_speaker(current_pitch)
                        pitch_str = f"{current_pitch:.2f} Hz" if current_pitch else "N/A"

                        temp_filename = "temp_live_audio.wav"
                        audio_data_int16 = (current_buffer_segment * 32767).astype(np.int16)
                        audio_segment = AudioSegment(
                            audio_data_int16.tobytes(), frame_rate=samplerate, sample_width=2, channels=1
                        )
                        audio_segment.export(temp_filename, format="wav")

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
                            if os.path.exists(temp_filename):
                                os.remove(temp_filename)

                        if text:
                            if last_speaker_id != self.current_speaker:
                                if self.current_segment_text.strip():
                                    print(f"=== Speaker {last_speaker_id} Finished ===")
                                    self.speaker_segments[last_speaker_id].append(self.current_segment_text.strip())
                                    self.initialize_agent_snippet()
                                    self.current_segment_text = ""
                            self.current_segment_text += " " + text

                            print(f"[Speaker {speaker_id}] (Pitch: {pitch_str}) (RMS: {rms_val:.4f}): {text}")

            except KeyboardInterrupt:
                print("\nStopping transcription...")
                if self.current_segment_text.strip():
                    self.speaker_segments[self.current_speaker].append(self.current_segment_text.strip())
                    self.initialize_agent_snippet()

                print("\n=== Full Conversation Summary ===")
                for spk, segments in self.speaker_segments.items():
                    print(f"\n--- Speaker {spk} ---")
                    for seg in segments:
                        print(seg)

            finally:
                if stream and not stream.closed:
                    stream.stop()
                    stream.close()
                    print("Audio stream closed.")
                if os.path.exists("temp_live_audio.wav"):
                    os.remove("temp_live_audio.wav")


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.transcribe_live()
    breakpoint()