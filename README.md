## MindVoice Study Data Collection Setup

Experiment and configuration files for PsychoPy incorporating the Lab Streaming Layer (LSL) for data collection.

## Pre-Requisites 
- Setup the Recording Environment by following [this guide](https://docs.google.com/document/d/1NA2v7Z6gLFAqDksrsyBf3V2RNZ6RxAdAVVEvcNDk-yA/edit?usp=sharing)
- Read through the [data collection protocol](https://docs.google.com/document/d/1cSVNwW5R3KIdb9JhpqlCfmGl2EIIykYLU7TWKvh_AH8/edit?usp=sharing) for this experiment
  
## Repository Structure

### Scripts
- The `scripts` folder contains useful scripts for sending audio recordings over LSL and evaluating and processing the data after the recording is complete.
  
### Stimuli
- The `stimuli` folder contains the words and sentences used as a stimulus for the experiment.
  
### Experiment Configurations
- `config.yaml` file contains the various configurations for accommodating different modalities in the experiment and handling the timings for various routines in the experiment.
- It currently supports three configurations: `eeg`, `fnirs`, `test`
- Each of the configurations has the following attributes:

```yaml
  baseline_duration: 30 # Duration of the baseline routine (in seconds)
  stimuli_repeats: 3 # Number of times each sound stimulus will repeat
  stimulus_duration: 3 # Duration of the stimulus routine (in seconds)
  imagine_duration: 5 # Duration of the imagine routine following the stimulus (in seconds)
  speak_duration: 5 # Duration of the speaking routine following the stimulus (in seconds)
  rest_range: [8, 12] # Duration range of the rest routine following the response (in seconds)
```
- Check the `config.yaml` file for the actual values for each configuration
  
### PsychoPy Configuration
- Experiment files:
  - `mindvoice-pt1.psyexp`: Experiment file for part 1 of the experiment (using words as a stimuli)
  - `mindvoice-pt2.psyexp`: Experiment file for part 2 of the experiment (using sentences as a stimuli)
- Before running the PsychoPy experiment, it expects a few inputs:
  - `participant`: A unique ID (number) for the participant. By default, it generates a random number which can be changed.
  - `run`: Run number for the same participant for the same experiment if multiple recordings are needed (usually 1)
  - `config`: The name of the experimental configuration value defined above.
  - `test_run`: A single run of the experiment to ensure all the settings are configured properly. Accepts either `true` or `false` as inputs. 

