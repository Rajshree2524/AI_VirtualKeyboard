import cv2
from cvzone.HandTrackingModule import HandDetector
import math
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finalText=""

keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, (button.pos), (x + w, y + h), (225, 0, 225), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img


class Button():
    def __init__(self, pos, text, size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)

        if len(hands) == 2:
            # Hand 2
            hand2 = hands[1]
            lmList2 = hand2["lmList"]  # List of 21 Landmark points
            bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
            centerPoint2 = hand2['center']  # center of the hand cx,cy
            handType2 = hand2["type"]  # Hand Type "Left" or "Right"
            fingers2 = detector.fingersUp(hand2)

        img=drawAll(img,buttonList)

        if lmList1:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    cv2.rectangle(img, (button.pos), (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    # Calculate distance manually
                    x1, y1 = lmList1[8][0], lmList1[8][1]
                    x2, y2 = lmList1[12][0], lmList1[12][1]
                    length = math.hypot(x2 - x1, y2 - y1)
                    info = (x1, y1, x2, y2, (x1 + x2) // 2, (y1 + y2) // 2)
                    #cv2.line(img, (x1, y1), (x2, y2), (175, 0, 175), 3)
                    #cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 15, (255, 0, 255), cv2.FILLED)
                    #cv2.putText(img, f"{int(length)}", ((x1 + x2) // 2 + 20, (y1 + y2) // 2), cv2.FONT_HERSHEY_PLAIN, 4,
                               # (255, 255, 255), 4)
                    if length<40:
                        keyboard.press(button.text)
                        cv2.rectangle(img, (button.pos), (x + w, y + h), (0, 225, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        finalText += button.text
                        sleep(0.15)

        cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 430),cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)