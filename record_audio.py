import pylsl
import pyaudio
import numpy as np

# Audio stream parameters
format = pyaudio.paInt16  # 16-bit format
channels = 1  # mono audio
rate = 44100  # sample rate in Hz
chunk_size = 1024  # number of audio samples per frame

# Create a PyAudio instance
p = pyaudio.PyAudio()

# LSL stream parameters
stream_name = 'AudioStream'
stream_type = 'Audio'
stream_id = 'my_audio_stream_1'

# Create LSL stream info
info = pylsl.StreamInfo(stream_name, stream_type,
                        channels, rate, pylsl.cf_int16, stream_id)

# Create LSL outlet
outlet = pylsl.StreamOutlet(info)

# Callback function to stream audio


def callback(in_data, frame_count, time_info, status):
    # Convert audio data to numpy array
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    # Push audio data into LSL stream
    outlet.push_chunk(audio_data.tolist())
    return (in_data, pyaudio.paContinue)


# Open stream with PyAudio
stream = p.open(format=format,
                channels=channels,
                rate=rate,
                input=True,
                frames_per_buffer=chunk_size,
                stream_callback=callback)

# Start the audio stream
stream.start_stream()

# Keep the stream open and pushing data
try:
    while stream.is_active():
        # You can do other things here if necessary
        pylsl.local_clock()  # Just to prevent the loop from being optimized out
except KeyboardInterrupt:
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PyAudio instance
    p.terminate()
