import pylsl
import pyaudio
import numpy as np


def list_and_select_device(p):
    """
    Lists all audio input devices that can record audio (excluding virtual devices) and
    prompts the user to select one for recording.
    Returns the index of the selected device.
    """
    print("Available recording devices:")
    valid_devices = []
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:  # Check if the device can record audio
            print(
                f"{len(valid_devices)}: {dev['name']} (Input Channels: {dev['maxInputChannels']})")
            valid_devices.append(i)
    device_index = int(input("Please select the device index for recording: "))
    if device_index < 0 or device_index >= len(valid_devices):
        raise ValueError("Invalid device index.")
    return valid_devices[device_index]


def create_lsl_stream(stream_name, stream_type, channels, rate, stream_id):
    """
    Creates and returns an LSL stream outlet based on the provided parameters.
    """
    info = pylsl.StreamInfo(stream_name, stream_type,
                            channels, rate, pylsl.cf_float32, stream_id)
    outlet = pylsl.StreamOutlet(info)
    return outlet


def audio_stream_callback(outlet, in_data, frame_count, time_info, status):
    """
    Callback function to stream audio data into LSL.
    Converts audio data to a numpy array and pushes it into the provided LSL stream outlet.
    """
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    outlet.push_chunk(audio_data.tolist())
    return (in_data, pyaudio.paContinue)


def test_recording(p, device_index, format, channels, rate, chunk_size):
    """
    Records a short audio clip from the selected device and plays it back to the user.
    """
    print("Testing recording for 3 seconds...")
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size,
                    input_device_index=device_index)
    frames = []
    for _ in range(0, int(rate / chunk_size * 3)):
        data = stream.read(chunk_size)
        frames.append(data)
    stream.close()

    print("Playing back the recorded audio...")
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)
    for data in frames:
        stream.write(data)
    stream.close()
    print("Test recording finished.")


def main():
    format = pyaudio.paInt16  # 16-bit format
    channels = 1  # mono audio
    rate = 44100  # sample rate in Hz
    chunk_size = 1024  # number of audio samples per frame

    p = pyaudio.PyAudio()

    while True:
        selected_device_index = list_and_select_device(p)

        test_option = input(
            "Do you want to test recording on this device? (y/n): ")
        if test_option.lower() == 'y' or test_option.lower() == '':
            test_recording(p, selected_device_index, format,
                           channels, rate, chunk_size)

        continue_option = input(
            "Continue with this device for LSL stream? (y/n): ")
        if continue_option.lower() == 'y' or continue_option.lower() == '':
            break

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
            pylsl.local_clock()  # Keep the loop active
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    main()
