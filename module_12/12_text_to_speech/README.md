# Text to Speech

## Project Overview
`text_to_speech.py` converts text from a file into spoken audio using the `pyttsx3` library. It demonstrates how to automate narration or quick message playback without an internet connection.

## Variables
`INPUT_TEXT` defines the path of the source text file and `OUTPUT_AUDIO` specifies where the generated WAV file will be saved.

## Instructions
Install `pyttsx3` with `pip install pyttsx3`. Place your text in `input.txt` or edit `INPUT_TEXT` in the script. Run `python text_to_speech.py` to create `speech.wav`.

## Explanation
`pyttsx3` is a cross-platform text-to-speech engine. The script reads the text file, initializes the engine, and writes the spoken output to a WAV file. This provides a simple way to vocalize any text content on demand.
