# Image Processing

## Project Overview
`process_images.py` applies a grayscale filter to all JPG files in the `images` directory using the Pillow library. Each processed image is written to `output` with the same filename.

## Variables
The script expects an `images` folder containing the source pictures and creates an `output` folder automatically.

## Instructions
Install Pillow with `pip install pillow`. Add your JPEG images to the `images` directory and run `python process_images.py`. The grayscale versions will appear in `output`.

## Explanation
Pillow's `Image.open` function loads each file. The `convert('L')` call transforms the picture into grayscale. Saving to a separate directory keeps the originals intact while providing a quick batch-processing workflow.
