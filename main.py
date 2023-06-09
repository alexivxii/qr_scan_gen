import cv2
import numpy as np
import qrcode
import zxingcpp
from barcode import Code128
from barcode import EAN13
from barcode import ISBN13
from barcode.writer import ImageWriter

#Commit Alex
def generate_qr_code(data, file_name):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Get the QR code image as a PIL image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a file using PIL
    qr_image.save(file_name)

# Generate a QR code and save it as an image
data = "Hello, World!"
file_name = "qr_code.png"
generate_qr_code(data, file_name)
print("QR code generated successfully.")


def scan_qr_code():
    capture = cv2.VideoCapture(0)

    while True:
        _, frame = capture.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Create a QR code detector
        qr_code_detector = cv2.QRCodeDetector()

        # Detect and decode QR codes in the frame
        decoded_data, points, _ = qr_code_detector.detectAndDecode(gray)

        # If a QR code is detected, print the decoded information
        if points is not None:
            print("QR Code Detected:")
            #print(decoded_data == "")
            print(decoded_data)

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #####display

        if(decoded_data != ""):

            ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # Find contours in the binary image
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Find the contour with the largest area
            max_area = 0
            max_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    max_contour = contour

            # Get the bounding rectangle of the largest contour
            x, y, w, h = cv2.boundingRect(max_contour)

            # Extract the QR code region from the original image
            qr_code = frame[y:y + h, x:x + w]

            cv2.imshow(' ',qr_code)

    # Release the capture and destroy all windows
    capture.release()
    cv2.destroyAllWindows()

def scan_barcode():
    #image = cv2.imread('BarcodeTest.jpg')
    capture = cv2.VideoCapture(0)

    while True:
        _, frame = capture.read()

        #Preprocessing
        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #blur = cv2.GaussianBlur(gray_frame, (5, 5), 0)
        #ret, final_frame = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        barcodes = zxingcpp.read_barcodes(frame)

        for barcode in barcodes:
            # print(barcode.data)
            info = barcode.text
            print(info)

        # Display the frame
        cv2.imshow("Barcode Scanner", frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

    # Release the capture and destroy all windows
    capture.release()
    cv2.destroyAllWindows()

def generate_barcode():
    choice = input("FOR BARCODE: Code128 - 1 / EAN13 - 2 / ISBN13 - 3 -> ")
    if choice == "1":
        data = input("Type the Code128 barcode's content: ")
        while(not data):
            data = input("Content can't be empty: ")
        barcode = Code128(data, writer=ImageWriter())
    elif choice == "2":
        data = input("Type the EAN13 barcode's content: ")
        while (not data):
            data = input("Content can't be empty: ")
        barcode = EAN13(data, writer=ImageWriter())
    elif choice == "3":
        data = input("Type the ISBN barcode's content: ")
        while (not data):
            data = input("Content can't be empty: ")
        barcode = ISBN13(data, writer=ImageWriter())
    else:
        print("Invalid barcode option")
        return

    file_name = input("Choose a file name: ")
    barcode.save(file_name)

def menu():
    choice = input("OPTIONS: 1 - SCAN QR CODE / 2 - SCAN BARCODE / 3 - GENERATE QR CODE / 4 - GENERATE BARCODE -> ")

    if choice == "1":
        scan_qr_code()
    elif choice == "2":
        scan_barcode()
    elif choice == "3":
        generate_qr_code("End of semester", "qr.png")
    elif choice == "4":
        generate_barcode()
    else:
        print("Invalid option")
        return

menu()
