# Object Detection Dashboard

This folder demonstrates how to build a simple webcam dashboard that highlights objects and keeps a running count of detections.

## Files

- `app.py` – Streams annotated video frames through a Flask server and plots a live bar chart.
- `model.py` – Loads a pretrained YOLOv5 model and runs inference on frames.
- `requirements.txt` – Python packages required to run the example.

## How It Works

Object detection models such as YOLOv5 predict bounding boxes and class labels for objects in an image. The example loads the lightweight `yolov5s` model provided by the Ultralytics repository. Each captured frame from the webcam is passed to the model.

### Frame Processing

Every frame is examined for detections. When the model returns a set of boxes, `app.py` draws rectangles and text labels onto the image using OpenCV. The same labels are counted to keep track of how many times each object appears in a given minute. A pandas DataFrame stores these counts and the `/chart` route displays them as a bar plot.

## Running the Dashboard

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the application:
   ```bash
   python app.py
   ```
3. Navigate to `http://localhost:8000` in a browser. The page displays the live video feed with bounding boxes. Below the video is a chart of detection counts per minute.

The chart updates as time passes, giving a quick view of which objects have been seen most frequently in the current session.

Use this setup to monitor people or packages and extend it with your own object detection model if desired.
