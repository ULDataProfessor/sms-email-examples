import cv2
import io
import time
import threading
from flask import Flask, Response, render_template_string
import pandas as pd
import matplotlib.pyplot as plt

from model import load_model, run_inference

app = Flask(__name__)

model = load_model()
cap = cv2.VideoCapture(0)

df_lock = threading.Lock()
counts = pd.DataFrame(columns=['label', 'count'])

HTML_PAGE = """
<!doctype html>
<title>Object Detection Dashboard</title>
<h1>Live Video</h1>
<img src="/video_feed" width="640" />
<h1>Detection Counts</h1>
<img src="/chart" width="640" />
"""


def update_counts(detections):
    global counts
    with df_lock:
        timestamp = pd.Timestamp.now().floor('T')
        for label in detections['name']:
            mask = (counts['label'] == label) & (counts.index == timestamp)
            if mask.any():
                counts.loc[mask, 'count'] += 1
            else:
                counts = pd.concat([
                    counts,
                    pd.DataFrame({'label': [label], 'count': [1]}, index=[timestamp])
                ])


def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        detections = run_inference(model, frame)
        update_counts(detections)
        for _, row in detections.iterrows():
            x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = row['name']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def generate_chart():
    with df_lock:
        recent = counts.groupby(['label', counts.index]).sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 4))
    if not recent.empty:
        recent.T.plot(kind='bar', ax=ax)
    ax.set_xlabel('Minute')
    ax.set_ylabel('Detections')
    ax.legend(title='Label')
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.read()


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/chart')
def chart():
    img = generate_chart()
    return Response(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
