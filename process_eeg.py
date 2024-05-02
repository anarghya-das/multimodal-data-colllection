import pyxdf
import numpy as np
import mne
import os


def segment_modalities_optimized(marker_timestamps, modality_timestamps, modality_data):
    """
    Optimized segmentation of data for a modality based on marker timestamps, accommodating different sampling rates.

    :param marker_timestamps: Timestamps of markers.
    :param modality_timestamps: Timestamps of the modality data.
    :param modality_data: Data of the modality to be segmented.
    :return: A list of data segments for the modality.
    """
    # Convert to numpy arrays for efficient computation
    marker_timestamps = np.array(marker_timestamps)
    modality_timestamps = np.array(modality_timestamps)

    # Find insertion points for each marker in the modality timestamps
    insert_points = np.searchsorted(modality_timestamps, marker_timestamps)
    segments = []
    for i in range(len(insert_points) - 1):
        # Extract and store the segment
        start_index = insert_points[i]
        end_index = insert_points[i + 1]
        segment = modality_data[start_index:end_index]
        segments.append(segment)

    # Handle the last segment, from the last marker to the end of the data stream
    if insert_points[-1] < len(modality_data):
        last_segment = modality_data[insert_points[-1]:]
        segments.append(last_segment)
    else:
        # If the last marker is exactly at or beyond the end of the data, append an empty segment
        segments.append([])

    return segments


def filter_markers(marker_dict, prefix='stim'):
    """
    Filter markers based on the prefix.
    """
    return {k: v for k, v in marker_dict.items() if k.startswith(prefix)}


if __name__ == "__main__":
    ROOT = "/Users/anarghya/Developer/eeg_data/multimodal-speech-eeg/"
    SUBJECT = "08"
    file_path = os.path.join(ROOT, SUBJECT, "part1", "sub-" +
                             SUBJECT, "sub-" + SUBJECT + "_task-words_run-001.xdf")
    data, header = pyxdf.load_xdf(file_path)

    data_types = ['EEG', 'Markers', 'Audio']
    assert len(data) == 3
    # check whether the data has 3 streams of type 'Markers', 'EEG' and 'Audio' index can be different
    assert all([d['info']['type'][0] in data_types for d in data])

    marker_stream = [d for d in data if d['info']['type'][0] == 'Markers'][0]
    eeg_stream = [d for d in data if d['info']['type'][0] == 'EEG'][0]
    audio_stream = [d for d in data if d['info']['type'][0] == 'Audio'][0]

    # Part 1
    stim_file = os.path.join('stimuli', 'stimuli_words.txt')
    labels = open(stim_file).read().splitlines()
    prefix = ['rest', 'stim',  'I', 'S']

    marker_names = np.array(marker_stream['time_series']).squeeze()
    marker_dict = {p: i for i, p in enumerate(np.unique(marker_names))}
    id_binding = {v: k for k, v in marker_dict.items()}
    category_mapping = {
        p: [v for k, v in marker_dict.items() if k.startswith(p)] for p in prefix}

    marker_timestamps = np.array(marker_stream['time_stamps'])
    modality_timestamps = np.array(eeg_stream['time_stamps'])
    insert_points = np.searchsorted(modality_timestamps, marker_timestamps)

    ch_labels = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1',
                 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']
    sampling_rate = int(eeg_stream['info']['nominal_srate'][0])
    info = mne.create_info(
        ch_names=ch_labels, sfreq=sampling_rate, ch_types='eeg')
    data = eeg_stream["time_series"].T
    raw = mne.io.RawArray(data, info)
    raw.set_montage('standard_1020')

    label_id_func = np.vectorize(marker_dict.get)
    events = np.zeros((len(insert_points), 3), dtype=int)
    events[:, 0] = insert_points
    events[:, 2] = label_id_func(marker_names)
    annot = mne.annotations_from_events(events, raw.info['sfreq'], id_binding)
    raw.set_annotations(annot)

    # imagine = mne.pick_events(events, include=category_mapping['S'])
    # epoch = mne.Epochs(raw, imagine, event_id=filter_markers(marker_dict, prefix='S'), tmin=-0.5, tmax=1.5, baseline=None, preload=True)
