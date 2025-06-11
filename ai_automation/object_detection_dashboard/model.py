import torch


def load_model():
    """Load a pretrained YOLOv5 model from the Ultralytics repository."""
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.eval()
    return model


def run_inference(model, frame):
    """Run object detection on a single frame.

    Parameters
    ----------
    model : torch.nn.Module
        The YOLOv5 model.
    frame : numpy.ndarray
        BGR image from OpenCV.

    Returns
    -------
    pandas.DataFrame
        Detection results with bounding boxes and labels.
    """
    results = model(frame)
    return results.pandas().xyxy[0]
