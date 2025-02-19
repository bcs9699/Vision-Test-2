from inference import InferencePipeline
import cv2
import os
from adafruit_servokit import ServoKit
import numpy as np

# Servo setup
kit = ServoKit(channels=16)
pan_servo = kit.servo[0]
tilt_servo = kit.servo[1]

# Servo movement limits
PAN_MIN, PAN_MAX = 0, 180
TILT_MIN, TILT_MAX = 0, 90

# Camera resolution (adjust based on your setup)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Initialize servos at center positions
pan_angle = (PAN_MAX - PAN_MIN) // 2
tilt_angle = (TILT_MAX - TILT_MIN) // 2
pan_servo.angle = pan_angle
tilt_servo.angle = tilt_angle

# Force ONNX Runtime to use CPU (bypass CUDA errors)
os.environ["ORT_API_PROVIDERS"] = "CPUExecutionProvider"

def map_value(value, in_min, in_max, out_min, out_max):
    # Scale a value from one range to another
    return int(np.interp(value, [in_min, in_max], [out_min, out_max]))

def adjust_servos(x, y):
    global pan_angle, tilt_angle

    # Map bounding box center to servo angles
    pan_angle = map_value(x, 0, CAMERA_WIDTH, PAN_MIN, PAN_MAX)
    tilt_angle = map_value(y, 0, CAMERA_HEIGHT, TILT_MIN, TILT_MAX)

    # Update servos
    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle

def my_sink(result, video_frame):
    # Display processed result if available
    if result and isinstance(result, dict):
        visualization = result.get("output")  # Using 'output' as it's in the keys
        predictions = result.get("Model Predictions")

        if visualization is not None:
            img = visualization.image.copy() if hasattr(visualization, 'image') else visualization.copy()
            
            if predictions and hasattr(predictions, 'xyxy'):
                try:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = predictions.xyxy[0]  # Get first detection
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    
                    # Compute the center of the bounding box
                    x_center = (x1 + x2) // 2
                    y_center = (y1 + y2) // 2

                    # Adjust servos to center on the drone
                    adjust_servos(x_center, y_center)

                    # Draw rectangle and label on the image
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    coord_text = f"({x_center}, {y_center})"
                    cv2.putText(img, coord_text, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                except Exception as e:
                    print(f"Error processing bbox: {e}")
            
            cv2.imshow("Workflow Output", img)
            cv2.waitKey(1)

try:
    pipeline = InferencePipeline.init_with_workflow(
        api_key="rmiW2PS5qiHAEvXaZdgE",
        workspace_name="drone-tracking-weehf",
        workflow_id="custom-workflow",
        video_reference=0,  # Use webcam
        max_fps=30,
        on_prediction=my_sink
    )
    pipeline.start()
    pipeline.join()
except Exception as e:
    print(f"Error: {e}")
finally:
    cv2.destroyAllWindows()
