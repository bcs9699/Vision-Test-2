from inference import InferencePipeline
import cv2
import os
from adafruit_servokit import ServoKit
import numpy as np

# Initialize servo controller for pan-tilt mechanism
kit = ServoKit(channels=16)
pan_servo = kit.servo[0]  # Pan servo on channel 0
tilt_servo = kit.servo[1] # Tilt servo on channel 1

# Define the range of motion limits for servos (in degrees)
PAN_MIN, PAN_MAX = 0, 180  # Pan servo can move 0-180 degrees
TILT_MIN, TILT_MAX = 0, 90 # Tilt servo limited to 0-90 degrees for stability

# Define camera resolution for coordinate mapping
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Center both servos at startup
pan_angle = (PAN_MAX - PAN_MIN) // 2
tilt_angle = (TILT_MAX - TILT_MIN) // 2
pan_servo.angle = pan_angle
tilt_servo.angle = tilt_angle

# Configure ONNX Runtime to use CPU instead of GPU
os.environ["ORT_API_PROVIDERS"] = "CPUExecutionProvider"

def map_value(value, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another.
    Example: map_value(50, 0, 100, 0, 180) would convert 50% to 90 degrees
    """
    return int(np.interp(value, [in_min, in_max], [out_min, out_max]))

def adjust_servos(x, y):
    """
    Adjusts servo positions based on target coordinates in camera frame.
    Args:
        x: x-coordinate in camera frame (0 to CAMERA_WIDTH)
        y: y-coordinate in camera frame (0 to CAMERA_HEIGHT)
    """
    global pan_angle, tilt_angle

    # Convert camera coordinates to servo angles
    pan_angle = map_value(x, 0, CAMERA_WIDTH, PAN_MIN, PAN_MAX)
    tilt_angle = map_value(y, 0, CAMERA_HEIGHT, TILT_MIN, TILT_MAX)

    # Move servos to track target
    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle

def my_sink(result, video_frame):
    """
    Callback function that processes each frame from the video stream.
    Handles object detection results and updates servo positions.
    Args:
        result: Dictionary containing detection results
        video_frame: Current frame from video stream
    """
    # Process frame only if valid results exist
    if result and isinstance(result, dict):
        visualization = result.get("output")  # Get processed frame
        predictions = result.get("Model Predictions")  # Get detection results

        if visualization is not None:
            # Handle different visualization formats
            img = visualization.image.copy() if hasattr(visualization, 'image') else visualization.copy()
            
            # Process detection if bounding box exists
            if predictions and hasattr(predictions, 'xyxy'):
                try:
                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = predictions.xyxy[0]  # Get first detection
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    
                    # Calculate center point of detected object
                    x_center = (x1 + x2) // 2
                    y_center = (y1 + y2) // 2

                    # Move servos to track object
                    adjust_servos(x_center, y_center)

                    # Visualize detection results
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                    coord_text = f"({x_center}, {y_center})"  # Show center coordinates
                    cv2.putText(img, coord_text, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error processing bbox: {e}")
            
            # Display the processed frame
            cv2.imshow("Workflow Output", img)
            cv2.waitKey(1)

try:
    # Initialize and start the object detection pipeline
    pipeline = InferencePipeline.init_with_workflow(
        api_key="rmiW2PS5qiHAEvXaZdgE",
        workspace_name="drone-tracking-weehf",
        workflow_id="custom-workflow",
        video_reference=0,  # Use webcam as video source
        max_fps=30,
        on_prediction=my_sink
    )
    pipeline.start()
    pipeline.join()
except Exception as e:
    print(f"Error: {e}")
finally:
    # Clean up resources
    cv2.destroyAllWindows()
