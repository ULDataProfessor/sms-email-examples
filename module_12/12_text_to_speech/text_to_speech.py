"""Convert text from a file to speech."""
from __future__ import annotations

from pathlib import Path
import pyttsx3

INPUT_TEXT = Path("input.txt")
OUTPUT_AUDIO = Path("speech.wav")


def main(input_path: Path = INPUT_TEXT, output_path: Path = OUTPUT_AUDIO) -> None:
    engine = pyttsx3.init()
    text = input_path.read_text()
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()


if __name__ == "__main__":
    main()
