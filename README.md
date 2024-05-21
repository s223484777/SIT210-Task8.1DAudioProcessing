# SIT210-Task8.1DAudioProccessing
 S306 SIT210 Task 7.2D, Control a few LEDs using voice recognition on a Raspberry Pi 5.

## Description
Control a few LEDs on the Raspberry Pi 5 GPIO via the power of voice! (Plus help from google voice services...)


The system uses a USB microphone connected to the Raspberry Pi to record audio samples to send to Google voice services, which then returns the text content of the audio.
The text is then split into individual words to be dealt with if they "wake" word is first in the recording. This code uses "system" to indicate the start of a command.

## How it Works
The listen loop is in charge of first adjusting for ambient noise during a 4 second window, followed by listening to the microphone and getting the voice recognition from the Google voice service.

This snippet uses the `speech_recognizer` microphone object as the `source` and adjusts the sensitivity to match the abient noise.
```python
with sr.Microphone() as source:
  recognizer.adjust_for_ambient_noise(source, duration=4)
```

This snippet obtains an audio recording, or times out if not voice is detected. The timeout is the amount of continuous lack of voice until the audio is complete, or the maximum wait time if nothing is heard.
A `WaitTimeoutError` can be ignored in this use case as it will continue to throw these errors while waiting for instructions.
```python
try:
  audio_data = recognizer.listen(source, timeout=1)
except sr.exceptions.WaitTimeoutError:
  continue
```

Once we have an audio recording with possible voice, we can then send it to Google's voice recognition service to convert the recording voice into a string, which can then be split into an array of words.
```python
try:
  text = recognizer.recognize_google(audio_data).split()
  # If the text array starts with the wake word, process the remaining command parts.
  if text[0] == "system":
    processCommand(text[1:])
except sr.RequestError as e: # Issue contacting the Google Speech Recognition Service
  print("Error: Could not request results from Google Speech Recognition service;")
except: # Other exceptions can be ignored
  continue
```
The `continue` keyword in python skips the rest of the code nested in a loop, so in my use case if the `waitTimeoutError` is caught, it will jump back to the start of the loop, or if the running variable has been unset (set to False) the loop will terminate.


We now need to find the last control word said (allows a user to correct themselves, "system, red on, wait off" will first see on, but correct it to off), as well as all the devices to control.
```python
for part in command:
  # For each part of the command array, determine what needs to be added to the
  # devices list to be controlled
  if part in leds.keys() and part not in devices_leds:
    devices_leds.append(part)
  elif part == "read" and "red" not in devices_leds:
    devices_leds.append("red")
  # If "all" is stated, all LEDs are added to the devices list
  elif part == "all":
    for led in leds.keys():
	  if led not in devices_leds:
	    devices_leds.append(led)
  # Set the control word (or reset if multiple are said)
  elif part in controls:
    control = part
  # Unrecognised words are printed out for debugging and review
  else:
    print(f"Unrecognised word: {part}")
```

Finally, we control the selected devices as per the voice coommand control word
```python
# Turn on the selected devices
if control == "on":
  print(f"{control}: {devices_leds}")
  for led in devices_leds:
    leds[led].on()
# Turn off the selected devices
elif control == "off":
  print(f"{control}: {devices_leds}")
  for led in devices_leds:
    leds[led].off()
# Unset running so that when we return to the listen loop, the while loop and
# ultimately the script will terminate
elif part == "terminate":
  running = False
```

Thanks to (Simplilearn)[https://www.simplilearn.com/tutorials/python-tutorial/speech-recognition-in-python] and (SpeechRecognition PyPI)[https://pypi.org/project/SpeechRecognition/] for the reference and documents to make this python functional.

## Usage
Simply say "system" followed by a control word and some devices, and the system will obey your commands.
Available control words are:
on - Turn the devcies on
off - Turn the devices off
terminate - Terminate the python script

Requires the following libraries:
* gpiozero
* speech_recognition
* sounddevice

## Task Name
The task name is "Task 7.2D Raspberry Pi Audio Processing" in the task sheet, however the repo is named according to the task sheet instructions as "Task8.1DAudioProcessing".