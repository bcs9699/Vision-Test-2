from inference import InferencePipeline
import cv2
import os

# Force ONNX Runtime to use CPU (bypass CUDA errors)
os.environ["ORT_API_PROVIDERS"] = "CPUExecutionProvider"

def my_sink(result, video_frame):
    # Display processed result if available
    if result and isinstance(result, dict):
        visualization = result.get("output")  # Using 'output' as it's in the keys
        bbox = result.get("Bounding Box")
        label = result.get("Label")
        predictions = result.get("Model Predictions")
        
        print("\nBounding Box:", bbox)
        print("Label:", label)
        print("Predictions:", predictions)
        
        if visualization is not None:
            if hasattr(visualization, 'numpy_image'):
                img = visualization.numpy_image.copy()
            elif hasattr(visualization, 'image'):
                img = visualization.image.copy()
            else:
                img = visualization.copy()
            
            # If we have predictions with bounding boxes
            if predictions and hasattr(predictions, 'xyxy'):
                try:
                    # Get coordinates from the xyxy array
                    x1, y1, x2, y2 = predictions.xyxy[0]  # Get first detection
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])  # Convert to integers
                    
                    # Draw rectangle
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Add coordinates and label text
                    coord_text = f"({x1}, {y1})"
                    if hasattr(predictions.data, 'class_name'):
                        class_name = predictions.data['class_name'][0]  # Get first class name
                        coord_text += f" {class_name}"
                    
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
    


