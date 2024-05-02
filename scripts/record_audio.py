import pyaudio
import numpy as np
from mne_lsl.lsl import StreamInfo, StreamOutlet, local_clock


def list_and_select_device(p):
    """
    Lists all available audio devices and prompts the user to select one for recording.
    Returns the index of the selected device.
    """
    print("Available recording devices:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        print(
            f"{i}: {dev['name']} (Input Channels: {dev['maxInputChannels']})")
    device_index = int(input("Please select the device index for recording: "))
    return device_index


def create_lsl_stream(stream_name, stream_type, channels, rate, stream_id):
    """
    Creates and returns an LSL stream outlet based on the provided parameters using mne_lsl.
    """
    info = StreamInfo(name=stream_name, stype=stream_type, n_channels=channels,
                      sfreq=rate, dtype='int16', source_id=stream_id)
    outlet = StreamOutlet(info)
    return outlet


def audio_stream_callback(outlet, in_data, frame_count, time_info, status):
    """
    Callback function to stream audio data into LSL using mne_lsl.
    Converts audio data to a numpy array and pushes it into the LSL stream via mne_lsl.
    """
    audio_data = np.frombuffer(in_data, dtype=np.int16).copy()
    audio_data = audio_data.reshape(-1, 1)
    outlet.push_chunk(audio_data)
    return (in_data, pyaudio.paContinue)


def main():
    format = pyaudio.paInt16  # 16-bit format
    channels = 1  # mono audio
    rate = 44100  # sample rate in Hz
    chunk_size = 1024  # number of audio samples per frame

    p = pyaudio.PyAudio()
    selected_device_index = list_and_select_device(p)

    stream_name = 'AudioStream'
    stream_type = 'Audio'
    stream_id = 'my_audio_stream_1'
    outlet = create_lsl_stream(
        stream_name, stream_type, channels, rate, stream_id)

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size,
                    input_device_index=selected_device_index,
                    stream_callback=lambda in_data, frame_count, time_info, status: audio_stream_callback(outlet, in_data, frame_count, time_info, status))

    stream.start_stream()

    try:
        while stream.is_active():
            local_clock()  # Looping to keep the stream active
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    main()
