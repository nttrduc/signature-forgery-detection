from ultralytics import YOLO
import cv2
import torch

with open('web/static/txt/image_paths.txt', 'r') as file:
    lines = file.readlines()
    # Xóa ký tự newline ở cuối mỗi dòng
lines = [line.strip() for line in lines]

# Load a model
model = YOLO("best_yolo.pt") 

# Run batched inference on a list of images
results = model(lines)

# Process results list
count = 0
for result in results:
    img = result.orig_img  # Original image
    boxes = result.boxes.xyxy  # Bounding box coordinates
    
    # Sort the boxes by y1 (the second value in the box)
    sorted_boxes = sorted(boxes, key=lambda box: box[1])
    
    # Extract the highest box (first box after sorting)
    if sorted_boxes:
        x1, y1, x2, y2 = map(int, sorted_boxes[0])
        
        # Crop the image to the bounding box
        cropped_img = img[y1:y2, x1:x2]
        
        # Save the cropped image
        cv2.imwrite("test_cycle_gan/image" + str(count) + ".jpg", cropped_img)
    count += 1
