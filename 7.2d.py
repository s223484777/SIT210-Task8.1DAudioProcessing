#!/usr/bin/env python

import speech_recognition as sr
import sounddevice
import gpiozero

# Allow easy termination of the main loop by setting running to False
running = True

# Configure the RGB LED pins
leds = {
  "red":   gpiozero.LED(19, active_high=False),
  "green": gpiozero.LED(13, active_high=False),
  "blue":  gpiozero.LED(12, active_high=False),
}

# Available controls
controls = ["on", "off", "terminate"]

# Create a Recognizer instance
recognizer = sr.Recognizer()

# Process the given command parts
def processCommand(command):
  global running
  control = ""
  devices_leds = []

  # Get LEDs and control words from the provided command
  for part in command:
    if part in leds.keys() and part not in devices_leds:
      devices_leds.append(part)
    elif part == "read" and "red" not in devices_leds:
      devices_leds.append("red")
    elif part == "all":
      for led in leds.keys():
        if led not in devices_leds:
          devices_leds.append(led)
    elif part in controls:
      control = part
    else:
      print(f"Unrecognised word: {part}")

  # Handle the control words
  if control == "on":
    print(f"{control}: {devices_leds}")
    for led in devices_leds:
      leds[led].on()
  elif control == "off":
    print(f"{control}: {devices_leds}")
    for led in devices_leds:
      leds[led].off()
  elif part == "terminate":
    running = False

# Run the listening loop
def listen():
  global running, recognizer
  with sr.Microphone() as source:
    # Adjust the source for ambient noise
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=4)
    print("Adjusted.")

    # Run the loop until terminated
    while running:
      # Listen or continue if nothing heard
      try:
        audio_data = recognizer.listen(source, timeout=1)
      except sr.exceptions.WaitTimeoutError:
        continue

      # use Google's voice recognition service
      try:
        text = recognizer.recognize_google(audio_data).split()
        if text[0] == "system":
          processCommand(text[1:])
      except sr.RequestError as e:
        print("Error: Could not request results from Google Speech Recognition service;")
      except:
        continue

if __name__ == "__main__":
  listen()
