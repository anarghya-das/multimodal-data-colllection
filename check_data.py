import sys
import os
import pyxdf
import soundfile as sf


def write_audio_data(audio_data_buffer, out_path='audio.wav'):
    audio_fs = 44100
    sf.write(out_path, audio_data_buffer, audio_fs)


def write_markers(maarker_stream_stims):
    with open('markers.txt', 'w') as f:
        for marker in maarker_stream_stims:
            f.write(f"{marker[0]}\n")


def check_data(data_path):
    data_types = ['EEG', 'Markers', 'Audio']
    if os.path.exists(data_path):
        data, _ = pyxdf.load_xdf(data_path)
        assert len(data) == 3, "Data does not contain 3 streams"
        # check whether the data has 3 streams of type 'Markers', 'EEG' and 'Audio' index can be different
        assert all([d['info']['type'][0] in data_types for d in data]
                   ), "Data does not contain required stream types"
        marker_stream = [d for d in data if d['info']
                         ['type'][0] == 'Markers'][0]
        eeg_stream = [d for d in data if d['info']['type'][0] == 'EEG'][0]
        audio_stream = [d for d in data if d['info']['type'][0] == 'Audio'][0]

        audio_data = audio_stream['time_series'].squeeze()
        write_audio_data(audio_data)
        write_markers(marker_stream['time_series'])
        print("Audio data written to audio.wav")
    else:
        print("Data file not found")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_data.py <path_to_data_file>")
        sys.exit(1)

    data_path = sys.argv[1]
    check_data(data_path)
