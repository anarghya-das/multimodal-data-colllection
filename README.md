## Data Collection Protocol Setup

#### Pre-requisites:

- **[Python](https://www.python.org/)**: You need Python installed on your system to run the scripts.
- **GitHub Repository:** Clone/download the repository as it contains all the necessary files. After cloning the repository, run: `pip install -r requirements.txt` to install the required Python packages.
- **[PsychoPy](https://www.psychopy.org/download.html)**
- **[Lab Recorder](https://github.com/labstreaminglayer/App-LabRecorder/releases):** Choose the executable for your operating system. Check [this page](https://github.com/labstreaminglayer/App-LabRecorder?tab=readme-ov-file#dependencies) for specific instructions for your operating system.
- **Scripts:** LSL Computer Audio Recorder (record_audio.py) and Testing Recorded Audio (test_audio_input.py)


#### Lab Recorder Configuration:

- Currently, there are some issues with setting up the lab recorder for Apple Silicon Macs. Follow [this guide]((https://github.com/labstreaminglayer/App-LabRecorder/issues/109)) to try to resolve it or use the Windows or Linux operating system.
- Ensure `RCS` is enabled and `RCS port` is set to `22345`
- Select an appropriate location for the study root
- Leave the rest of the fields unchanged

#### Audio Recording Script:

- Download and run the Computer Audio Recorder (LSL) script.
- Run the script: `python3 record_audio.py`
- To stop the script, press `Ctrl+C` once the experiment is finished.

#### EEG Recording Configuration:

##### OpenBCI:

- Open the OpenBCI GUI and configure it according to your hardware specifications.
- Select Data source, Transfer protocol, and ensure that 16 channels are selected if available.
- Start the session and ensure proper impedance levels for good signal quality.

##### fNIRS:
- 

#### PsychoPy Configuration:
- Run PsychoPy and open the experiment file (ending with `.psyexp`) from the cloned Github repository.
- You should see the following screen if everything is loaded correctly: [img](#)
- If you are using multiple monitors, you can select the display where you want the experiment to run by clicking the settings button (gear icon in the screenshot below), choosing the screen tab, and entering the screen number in the text box. You can click on the “show screen numbers” button to identify the screen numbers for each screen. All the buttons and inputs required to perform this are highlighted in red in the screenshot below. [img](#)
- To test the setup, you can set the value of `test_run` input to `true` when you run the experiment (it is case-sensitive; make sure it's all lowercase).
  - This will execute the stimuli loop once, enabling you to promptly verify the correct display of stimuli on the screen and ensure that the lab recorder stops and saves the data accurately after the experiment completes
  - Applicable to both parts of the experiment [img](#)


### Running the Experiment:

- Ensure all applicable components (EEG recording device, Audio Recording Scripts, and PsychoPy) are correctly configured and running.
  - Make sure the EEG recording device, audio recorder script and Lab Recorder application are running before starting the experiment from Psychopy
PsychoPy is the primary application used to run the experiment 
For part 1, open the mindvoice-pt1.psyexp file, and for part 2, open the mindvoice-pt2.psyexp file in Psychopy
   
- Start the experiment from PsychoPy and monitor both the experiment and Lab Recorder.
- After the experiment, ensure the data is properly recorded and stored in the specified Study Root.
