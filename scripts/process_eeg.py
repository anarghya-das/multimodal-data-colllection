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


def list_folders(path):
    return [directory for directory in os.listdir(path) if os.path.isdir(os.path.join(path, directory))]


def get_xdf(path):
    return [file for file in os.listdir(path) if file.endswith(".xdf")]


if __name__ == "__main__":
    ROOT = "/Users/anarghya/Developer/eeg_data/multimodal-speech-eeg/dku"
    subjects = list_folders(ROOT)
    ch_labels = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1',
                 'O2', 'F7', 'F8', 'F3', 'F4', 'T7', 'T8', 'P3', 'P4']

    for subject in subjects:
        try:
            subject_folder = os.path.join(ROOT, subject)
            exp_parts = list_folders(subject_folder)
            for exp in exp_parts:
                print(f"Processing {subject}-{exp}...")
                xdf_path = get_xdf(os.path.join(subject_folder, exp))[0]
                data, header = pyxdf.load_xdf(
                    os.path.join(subject_folder, exp, xdf_path), select_streams=[{'type': 'EEG'}, {'type': 'Markers'}])

                marker_stream = [d for d in data if d['info']
                                 ['type'][0] == 'Markers'][0]
                eeg_stream = [d for d in data if d['info']
                              ['type'][0] == 'EEG'][0]
                # audio_stream = [d for d in data if d['info']
                #                 ['type'][0] == 'Audio'][0]
                prefix = ['rest', 'stim',  'I', 'S']
                if exp == 'part-2':
                    prefix = ['rest', 'imagine', 'speak']

                marker_names = np.array(
                    marker_stream['time_series']).squeeze()
                marker_dict = {p: i for i, p in enumerate(
                    np.unique(marker_names))}
                id_binding = {v: k for k, v in marker_dict.items()}
                category_mapping = {
                    p: [v for k, v in marker_dict.items() if k.startswith(p)] for p in prefix}

                marker_timestamps = np.array(marker_stream['time_stamps'])
                modality_timestamps = np.array(eeg_stream['time_stamps'])
                insert_points = np.searchsorted(
                    modality_timestamps, marker_timestamps)

                sampling_rate = int(eeg_stream['info']['nominal_srate'][0])
                info = mne.create_info(
                    ch_names=ch_labels, sfreq=sampling_rate, ch_types='eeg')
                data = eeg_stream["time_series"].T
                raw = mne.io.RawArray(data, info)
                raw.set_montage('standard_1020')
                # Apply bandpass filter
                raw = raw.filter(l_freq=0.3, h_freq=60)
                # Apply notch filter
                raw = raw.notch_filter(freqs=50)

                label_id_func = np.vectorize(marker_dict.get)
                events = np.zeros((len(insert_points), 3), dtype=int)
                events[:, 0] = insert_points
                events[:, 2] = label_id_func(marker_names)
                annot = mne.annotations_from_events(
                    events, raw.info['sfreq'], id_binding)
                raw.set_annotations(annot)

                raw.plot(scalings='auto', events=events, block=True)
                # save the raw data
                raw.save(os.path.join(subject_folder,
                                      exp, f'{subject}_eeg.fif'), overwrite=True)
        except Exception as e:
            print(f"Error processing {subject}-{exp}")
            open(os.path.join(subject_folder,
                              exp, f'{subject}_error.txt'), 'w').write(str(e))
        # imagine = mne.pick_events(events, include=category_mapping['S'])
        # epoch = mne.Epochs(raw, imagine, event_id=filter_markers(marker_dict, prefix='S'), tmin=-0.5, tmax=1.5, baseline=None, preload=True)
