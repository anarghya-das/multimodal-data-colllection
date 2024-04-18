## Data Collection Protocol Setup

#### Pre-requisites:

- **GitHub Repository:** Clone/download the repository as it contains all the necessary files. After cloning the repository, run: `pip install -r requirements.txt` to install the required Python packages.
- **[PsychoPy](https://www.psychopy.org/download.html)**
- **[Lab Recorder](https://github.com/labstreaminglayer/App-LabRecorder/releases):** Choose the executable for your operating system. Check [this page](https://github.com/labstreaminglayer/App-LabRecorder?tab=readme-ov-file#dependencies) for specific instructions for your operating system.
- **Scripts:** Computer Audio Recorder (LSL)


#### Lab Recorder Configuration:

- There are some issues when setting up lab recorder for apple silicon macs. Follow [this guide]((https://github.com/labstreaminglayer/App-LabRecorder/issues/109)) to try to resolve it or just use windows or linux operating system.
- Ensure `RCS` is enabled and `RCS port` is set to `22345`
- Select an appropriate location for the study root
- Leave the rest of the fields unchanged

#### Audio Recording Script:

- Download and run the Computer Audio Recorder (LSL) script.
- Follow video demo instructions to set up audio recording.
- To stop the script, press `Ctrl+C` once the experiment is finished.

#### EEG Recording Configuration (OpenBCI GUI):

- Open the OpenBCI GUI and configure according to your hardware specifications.
- Select Data source, Transfer protocol, and ensure that 16 channels are selected if available.
- Start the session and ensure proper impedance levels for good signal quality.

#### PsychoPy Configuration:

- Download the experiment and prompts file.
- Create a new folder for the experiment and move all downloaded files there.
- Open the `.psyexp` file in PsychoPy and configure the display settings.

### Running the Experiment:

- Ensure all components are correctly configured and running.
- Start the experiment from PsychoPy and monitor both the experiment and Lab Recorder.
- After the experiment, ensure the data is properly recorded and stored in the specified Study Root.
