import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 # Load cascade classifier
cap = cv2.VideoCapture(0) # Open default camera

while True:
    ret, img = cap.read() # Read image from camera
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # Detect faces using cascade classifier
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) # Draw rectangle around the face
    cv2.imshow('img',img) # Show image
    if cv2.waitKey(1) & 0xFF == ord('q'): # Quit if 'q' is pressed
        break

cap.release() # Release camera
cv2.destroyAllWindows() # Destroy all windows
