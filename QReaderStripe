# -*- coding: utf-8 -*-
import zbar
import time
import stripe
import json
import pyfirmata

from PIL import Image
import cv2

DELAY = 0.1
PORT = '/dev/ttyACM0'
board = pyfirmata.Arduino(PORT)

stripe.api_key = "sk_test_terqo3Zp0zM6LuP6rhCLXUSU"
lastCall = time.time()

def main():
    """
    A simple function that captures webcam video utilizing OpenCV. The video is then broken down into frames which
    are constantly displayed. The frame is then converted to grayscale for better contrast. Afterwards, the image
    is transformed into a numpy array using PIL. This is needed to create zbar image. This zbar image is then scanned
    utilizing zbar's image scanner and will then print the decodeed message of any QR or bar code. To quit the program,
    press "q".
    :return:
    """
    
    # Begin capturing video. You can modify what video source to use with VideoCapture's argument. It's currently set
    # to be your webcam.
    capture = cv2.VideoCapture(0)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
       
        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tostring())
        
        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        for decoded in zbar_image:
            global lastCall
            comparison = time.time() - lastCall
            if (comparison > 3):
                print(decoded.data)
                print(comparison)
                checkForSubStatus(decoded.data)
              
        
def checkForSubStatus(customerID):
    global lastCall
    activeSubs = 0
    
    print("Retrieve will start")
    customer = stripe.Customer.retrieve(customerID)
    subscriptions = customer['subscriptions']
    data = subscriptions['data']

    for sub in data:
        if (sub['status'] == "active"):
            activeSubs = activeSubs + 1
        elif (sub['status'] == "trialing"):
            activeSubs = activeSubs - 1
        elif (sub['status'] == "unpaid"):
            activeSubs = activeSubs - 1
        elif (sub['status'] == "past_due"):
            activeSubs = activeSubs - 1

    if activeSubs == len(data):
        print("Todo está al corriente")
        board.digital[13].write(1)
        board.pass_time(DELAY)
        board.digital[13].write(0)
        lastCall = time.time()
    else:
        print("Pagos pendientes")
        board.digital[12].write(1)
        board.pass_time(DELAY)
        board.digital[12].write(0)
        lastCall = time.time()
    
if __name__ == "__main__":
    main()
