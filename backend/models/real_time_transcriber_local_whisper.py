import os
import queue
import threading
import concurrent.futures
import sounddevice as sd
import numpy as np
import librosa
import asyncio
import websockets
from faster_whisper import WhisperModel


class RealTimeTranscriber:
    def __init__(self, ws_port=8765):
        self.q = queue.Queue()
        self.model = WhisperModel("base.en", compute_type="int8", num_workers=2)
        self.max_speakers = 2
        self.speaker_profiles = {1: [], 2: []}
        self.current_speaker = 1
        self.pitch_threshold = 30
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.ws_port = ws_port
        self.clients = set()
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self._start_ws_loop, daemon=True).start()

    def _start_ws_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start_ws_server())
        self.loop.run_forever()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(indata.copy())

    def get_pitch(self, audio_data, samplerate):
        try:
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            f0, voiced_flag, _ = librosa.pyin(audio_data,
                                              fmin=librosa.note_to_hz('C2'),
                                              fmax=librosa.note_to_hz('C7'),
                                              sr=samplerate)
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
            return 1

        if not self.speaker_profiles[2]:
            mean1 = np.mean(self.speaker_profiles[1])
            if abs(current_pitch - mean1) > self.pitch_threshold:
                self.speaker_profiles[2].append(current_pitch)
                self.current_speaker = 2
            else:
                self.speaker_profiles[1].append(current_pitch)
                self.current_speaker = 1
            return self.current_speaker

        mean1 = np.mean(self.speaker_profiles[1])
        mean2 = np.mean(self.speaker_profiles[2])

        if abs(current_pitch - mean1) <= abs(current_pitch - mean2):
            self.speaker_profiles[1].append(current_pitch)
            self.current_speaker = 1
        else:
            self.speaker_profiles[2].append(current_pitch)
            self.current_speaker = 2

        return self.current_speaker

    def process_audio_chunk(self, current_buffer):
        rms = np.sqrt(np.mean(current_buffer ** 2))
        if rms < 0.004:
            return

        audio_data = current_buffer.flatten().astype(np.float32)
        current_pitch = self.get_pitch(audio_data, 16000)
        if current_pitch is None:
            return

        speaker_id = self.identify_speaker(current_pitch)
        pitch_str = f"{current_pitch:.2f} Hz"

        segments, _ = self.model.transcribe(audio_data, language="en")

        for segment in segments:
            if segment.text.strip():
                message = f"[Speaker {speaker_id}] (Pitch: {pitch_str}): {segment.text.strip()}"
                print(message)
                asyncio.run_coroutine_threadsafe(self.broadcast(message), self.loop)

    async def broadcast(self, message):
        if self.clients:
            await asyncio.gather(*(client.send(message) for client in self.clients))

    async def ws_handler(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)

    async def start_ws_server(self):
        self.ws_server = await websockets.serve(self.ws_handler, "0.0.0.0", self.ws_port)
        print(f"WebSocket server started on ws://0.0.0.0:{self.ws_port}")

    def transcribe_live(self):
        samplerate = 16000
        blocksize = 2048
        duration = 2.0

        print("Start speaking... (Press CTRL+C to stop)")

        stream = sd.InputStream(
            samplerate=samplerate,
            blocksize=blocksize,
            channels=1,
            dtype="float32",
            callback=self.audio_callback
        )

        with stream:
            buffer = np.empty((0, 1), dtype=np.float32)

            try:
                while True:
                    audio_chunk = self.q.get()
                    buffer = np.concatenate((buffer, audio_chunk))

                    if len(buffer) >= int(samplerate * duration):
                        current_buffer = buffer[:int(samplerate * duration)]
                        buffer = buffer[int(samplerate * duration):]
                        self.executor.submit(self.process_audio_chunk, current_buffer)

            except KeyboardInterrupt:
                print("\nStopping transcription...")
            finally:
                if stream and not stream.closed:
                    stream.stop()
                    stream.close()
                    print("Audio stream closed.")
                self.executor.shutdown(wait=True)


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.transcribe_live()
