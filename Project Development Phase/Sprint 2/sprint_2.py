# prerequisites:
# pip install opencv-python
# pip install mediapipe
# pip install cvzone

# import the opencv library
import cv2
import time
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)

# uploading radiology images

zero = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_images\1.jpg'),
                  (1920, 1080))
one = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_images\2.jpg'),
                 (1920, 1080))
two = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_images\3.jpg'),
                 (1920, 1080))
three = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_imagess\4.jpg'),
                   (1920, 1080))
four = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_imagess\5.jpg'),
                  (1920, 1080))
five = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_imagess\6.jpg'),
                  (1920, 1080))
six = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\radiology_images\7.jpg'),
                 (1920, 1080))

# uploading background image

background = cv2.resize(cv2.imread(
    r'C:\Users\ADMIN\OneDrive\Desktop\Gesture based tool\IBM-Project-43230-1660714426-main 3\Project Development Phase\sprint_2\dataset\background_image\background.png'),
                        (1920, 1080))

# creating two variables with values corresponding to the orgin of images
# used for zooming purposes
a = 960
b = 540

# putting all the images into an array
index = 0
images = [zero, one, two, three, four, five, six]

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_BUFFERSIZE, 1)
fing = -1

buf = images[index]

# Set the properties of GUI app
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while (True):
    ret, frame = vid.read()

    # Display the resulting frame
    img = cv2.flip(frame, 1)
    img = cv2.resize(img, (100, 100))
    background[:, :] = cv2.resize(buf, (1920, 1080))
    background[0:100, 0:100] = img
    cv2.imshow('image', background)
    # cv2.imshow('frame1', buf)
    hand = detector.findHands(img, draw=False)

    if fing != -1:
        fing = -1
        continue

    if hand:
        lmlist = hand[0]
        if lmlist:
            fingerup = detector.fingersUp(lmlist)

            # if little finger and ring-finger is raised, images are rotated in clockwise
            if fingerup == [0, 0, 0, 1, 1]:
                fing, a, b = -2, 960, 540
                # cv2.destroyWindow('frame1')
                buf = cv2.rotate(images[index], cv2.ROTATE_90_CLOCKWISE)
                print(fing)
                time.sleep(1)

            # if little finger, ring-finger and middle-finger is raised, images are rotated in anti-clockwise
            if fingerup == [0, 0, 1, 1, 1]:
                fing, a, b = -3, 960, 540
                # cv2.destroyWindow('frame1')
                buf = cv2.rotate(images[index], cv2.ROTATE_90_COUNTERCLOCKWISE)
                print(fing)
                time.sleep(1)

            # if index finger and little finger is raised, the app will quit
            if fingerup == [0, 1, 0, 0, 1]:
                break

            # if index finger is raised, the image will get zoomed  in
            if fingerup == [0, 1, 0, 0, 0]:
                # cv2.destroyWindow('frame1')
                b = b - 50
                a = a - 50
                buf = buf[960 - a:960 + a, 540 - b:540 + b]
                fing = 1
                print(fing)
                time.sleep(1)

            # when the index finger and middle fingers are raised, if the image was already zoomed in, the image will get zoomed out
            if fingerup == [0, 1, 1, 0, 0]:
                # cv2.destroyWindow('frame1')
                fing, a, b = 2, 960, 540
                buf = images[index]
                print(fing)
                time.sleep(1)

            # if the  index finger, middle finger,and ring finger is raised, the application will go to the last image
            if fingerup == [0, 1, 1, 1, 0]:
                fing, a, b = 3, 960, 540
                index = len(images) - 1
                buf = images[index]
                print(fing)
                time.sleep(1)

            # if the  index finger, middle finger,ring finger and littlefinger is raised, the application will go to the next image
            if fingerup == [0, 1, 1, 1, 1]:
                fing, a, b = 4, 960, 540
                # cv2.destroyWindow('frame1')
                index = index + 1
                if index == len(images): index = 0
                buf = images[index]
                print(fing)
                time.sleep(1)

            # if five fingers are raised, the application will go to the previous image
            if fingerup == [1, 1, 1, 1, 1]:
                fing, a, b = 5, 960, 540
                # cv2.destroyWindow('frame1')
                index = index - 1
                if index == -len(images) - 1: index = len(images) - 1
                buf = images[index]
                print(fing)
                time.sleep(1)

            # if the  thumb and little finger are raised, the application will go to the first image
            if fingerup == [1, 0, 0, 0, 1]:
                fing, a, b = 3, 960, 540
                index = 0
                buf = images[index]
                print(fing)
                time.sleep(1)
    else:
        print(fing)

    # if the key 'q' is pressed, the application will quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()