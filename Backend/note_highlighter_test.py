import easyocr
import cv2

# Load the image
img = cv2.imread('img2.jpg')

# Initialize the EasyOCR reader with English language
reader = easyocr.Reader(['en'])

# Perform OCR on the image and get the detail information including bounding boxes
results = reader.readtext(img, detail=1)

# Print all the detected words
print("Detected Words:")
for result in results:
    text = result[1]
    confidence = result[2]
    print(f"Word: {text}, Confidence: {confidence}")

# Create an overlay image as a copy of the original image
overlay = img.copy()

# Get the inputted string to search and highlight
input_string = input("Enter the string to highlight: ")

# Split the inputted string into individual words
input_words = input_string.lower().split()

# Iterate over the OCR results
for result in results:
    # Get the current detected word
    detected_word = result[1].lower()

    # Check if the current detected word matches any word in the inputted string
    if any(word in detected_word for word in input_words):
        # Get the bounding box coordinates
        bbox = result[0]
        x, y, w, h = bbox[0][0], bbox[0][1], bbox[2][0] - bbox[0][0], bbox[2][1] - bbox[0][1]

        # Draw a filled rectangle around the detected word with the correct size and color
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 0, 255), -1)

# Blend the overlay image with the original image
alpha = 0.4
img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

# Calculate the aspect ratio for resizing
aspect_ratio = img.shape[1] / img.shape[0]

# Set the width for resizing and calculate the corresponding height
width = 1000
height = int(width / aspect_ratio)

# Resize the resulting image
resized = cv2.resize(img_new, (width, height), interpolation=cv2.INTER_AREA)

# Display the resized image
cv2.imshow('img', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
