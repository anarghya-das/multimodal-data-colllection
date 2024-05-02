import pyaudio


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

# record audio using the selected device and play it back for 3 seconds


def record_audio(p, device_index):
    """
    Records audio from the selected device for 3 seconds and plays it back.
    """
    format = pyaudio.paInt16  # 16-bit format
    channels = 1  # mono audio
    rate = 44100  # sample rate in Hz
    chunk_size = 1024  # number of audio samples per frame
    duration = 3  # recording duration in seconds

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk_size,
                    input_device_index=device_index)

    print("Recording audio...")
    frames = []
    for i in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
    print("Finished recording.")

    stream.stop_stream()
    stream.close()

    # play back the recorded audio
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    output=True)
    print("Playing back audio...")
    for frame in frames:
        stream.write(frame)
    print("Finished playback.")

    stream.stop_stream()
    stream.close()


def main():
    p = pyaudio.PyAudio()
    selected_device_index = list_and_select_device(p)
    record_audio(p, selected_device_index)
    p.terminate()


if __name__ == "__main__":
    main()
