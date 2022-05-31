import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm


def painter():
    #######################
    brushThickness = 25
    eraserThickness = 100
    ########################

    # folderPath = "Header"
    # myList = os.listdir(folderPath)
    # print(myList)
    overlayList = []
    image = cv2.imread('background.png')
    # cursor = cv2.imread('Documents/cursor.png')
    # pencil = cv2.imread('Documents/pencil.png')
    # for imPath in myList:
    #     image = cv2.imread(f'{Documents}/{imPath}')
    #     overlayList.append(image)
    # print(len(overlayList))
    # header = overlayList[0]
    drawColor = (255, 0, 255)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = htm.handDetector(detectionCon=0.65, maxHands=1)
    xp, yp = 0, 0
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    clear = False

    while True:

        # 1. Import image
        success, img = cap.read()
        img = cv2.flip(img, 1)

        # 2. Find Hand Landmarks
        img = detector.findHands(img)

        lmList = detector.findPosition(img, draw=False)
        # lmList = hands[0]['lmList']

        if len(lmList[0]) != 0:

            # print(lmList)

            # tip of index and middle fingers
            x1, y1 = lmList[0][8][1:]
            x2, y2 = lmList[0][12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            # print(fingers)

            # # 4. If Submit Mode - Tumbs up
            # if fingers[0] and (fingers[2] == False) and (fingers[3] == False) and (fingers[4] == False) and (fingers[1] == False):
            #     cv2.putText(img, "Letter submited", (700, 70), cv2.FONT_HERSHEY_PLAIN, 3,
            #                 (0, 0, 255), 3)
            #     clear = True

            if fingers[1] and fingers[2]:
                xp, yp = 0, 0

                # cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                #               drawColor, cv2.FILLED)

                # xp, yp = 0, 0
                # print("Selection Mode")
                # # Checking for the click
                if y1 > 580:
                    if 20 < x1 < 580:
                        clear = True
                    elif 700 < x1 < 1260:
                        cv2.putText(img, "Bogstav indtastet", (700, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (0, 255, 0), 3)
                        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
                        _, imgInv = cv2.threshold(
                            imgGray, 50, 255, cv2.THRESH_BINARY_INV)
                        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
                        # cv2.imshow("Inv", imgInv)
                        cv2.imwrite('letter.jpg', imgInv)
                        clear = True
                        break

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                              (255, 255, 255), cv2.FILLED)
                x1 = y1 = 0

            # 5. If Drawing Mode - Index finger is up
            if fingers[1] and fingers[2] == False:

                cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
                # print("Drawing Mode")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

                # if drawColor == (0, 0, 0):
                #     cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                #     cv2.line(imgCanvas, (xp, yp), (x1, y1),
                #              drawColor, eraserThickness)

                else:
                    cv2.line(img, (xp, yp), (x1, y1),
                             drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1),
                             drawColor, brushThickness)

                xp, yp = x1, y1

            # Clear Canvas when all fingers are up
            if clear:
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)
                clear = False

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        # Setting the header image
        img[600:720, 0:1280] = image
        # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        cv2.imshow("Image", img)

        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)
