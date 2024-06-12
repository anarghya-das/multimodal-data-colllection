import sys
import os
import pyxdf
import soundfile as sf
import numpy as np


def write_audio_data(audio_data_buffer, out_path='audio.wav'):
    audio_fs = 44100
    sf.write(out_path, audio_data_buffer, audio_fs)


def write_markers(maarker_stream_stims, out_path='markers.txt'):
    with open(out_path, 'w') as f:
        for marker in maarker_stream_stims:
            f.write(f"{marker[0]}\n")


def calculate_nans(data):
    n_nans = np.sum(np.isnan(data))
    perc_nans = n_nans / len(data) * 100
    return n_nans, perc_nans


def write_data(audio, markers, data_path="temp_data"):
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    write_audio_data(audio, out_path=os.path.join(data_path, 'audio.wav'))
    # write_markers(markers['time_series'],
    #   out_path=os.path.join(data_path, 'markers.txt'))
    print(f"Audio data written to {os.path.join(data_path, 'audio.wav')}")


def check_data(data_path):
    data_types = ['EEG', 'Markers', 'Audio']
    if os.path.exists(data_path):
        data, _ = pyxdf.load_xdf(data_path)
        stream_names = [d['info']['name'][0] for d in data]
        print('Data contains the following streams: ', stream_names)
        # assert len(data) == 3, "Data does not contain 3 streams"
        # # check whether the data has 3 streams of type 'Markers', 'EEG' and 'Audio' index can be different
        # assert all([d['info']['type'][0] in data_types for d in data]
        #            ), "Data does not contain required stream types"
        print([d['info']['type'][0] for d in data])
        marker_stream = None
        eeg_stream = None
        audio_stream = None

        for d in data:
            if d['info']['type'][0] == 'Markers' and marker_stream is None:
                marker_stream = d
            elif d['info']['type'][0] == 'EEG' and eeg_stream is None:
                eeg_stream = d
            elif d['info']['type'][0] == 'Audio' and audio_stream is None:
                audio_stream = d

        audio_data = audio_stream['time_series'].squeeze()
        audio_nans, audio_nans_percentage = calculate_nans(audio_data)
        # eeg_nans, eeg_nans_percentage = calculate_nans(
        #     eeg_stream['time_series'])
        print(
            f"Audio data contains {audio_nans} nans ({audio_nans_percentage: .2f} %)")
        # print(
        #     f"EEG data contains {eeg_nans} nans ({eeg_nans_percentage: .2f} %)")

        write_data(audio_data, marker_stream)
    else:
        print("Data file not found")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_data.py <path_to_data_file>")
        sys.exit(1)

    data_path = sys.argv[1]
    check_data(data_path)
