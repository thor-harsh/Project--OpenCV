import cv2
import numpy as np
import sys


class OpenCV_Camera_Video_Utils:
    def __init__(self):
        pass

    def CameraAccess(self):
        s = 0
        if len(sys.argv) > 1:
            s = int(sys.argv[1])

        source = cv2.VideoCapture(s)
        win_name = 'Camera Preview'
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

        capture_image = False  # Variable to track image capture

        while True:
            key = cv2.waitKey(1)
            if key == 27:  # 'Esc' key to exit
                break
            elif key == ord(' '):  # 'Space' key to capture image
                capture_image = True

            has_frame, frame = source.read()
            if not has_frame:
                break
            frame = cv2.flip(frame, 2)

            cv2.imshow(win_name, frame)

            if capture_image:
                image_filename = "captured_image.jpg"
                cv2.imwrite(image_filename, frame)
                print(f"Image captured and saved as {image_filename}")
                capture_image = False  # Reset the flag after capturing

        source.release()
        cv2.destroyWindow(win_name)

    def VideoReader(self, videoPath):
        # source = 0  # source = 0 for webcam
        source = videoPath
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        win_name = 'Video Preview'
        cv2.namedWindow(win_name, cv2.WINDOW_FULLSCREEN)
        while cv2.waitKey(1) != 27:  # escape
            has_frame, frame = cap.read()
            if not has_frame:
                break
            cv2.imshow(win_name, frame)
        cap.release()
        cv2.destroyWindow(win_name)

    def VideoWriter(self):
        source = 0  # for webcam
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        win_name = 'Camera Preview'
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        print(frame_width, frame_height)

        # out_avi = cv2.VideoWriter("new_vid.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (frame_width, frame_height))
        out_mp4 = cv2.VideoWriter("new_video.mp4", cv2.VideoWriter_fourcc(*"XVID"), 30, (frame_width, frame_height))

        while cv2.waitKey(1) != 27:  # escape
            ret, frame = cap.read()
            if ret:
                out_mp4.write(frame)
                cv2.imshow(win_name, frame)
            else:
                break
        cap.release()
        out_mp4.release()
        cv2.destroyWindow(win_name)

    def WebCamFilter(self):
        PREVIEW = 0  # Preview Mode
        BLUR = 1  # Blurring Filter
        FEATURES = 2  # Corner Feature Detector
        CANNY = 3  # Canny Edge Detector

        s = 0
        if len(sys.argv) > 1:
            s = int(sys.argv[1])

        image_filter = PREVIEW
        alive = True
        win_name = "Camera Filters"
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

        source = cv2.VideoCapture(s)

        while alive:
            has_frame, frame = source.read()
            if not has_frame:
                break

            frame = cv2.flip(frame, 1)

            if image_filter == PREVIEW:
                result = frame
            elif image_filter == CANNY:
                result = cv2.Canny(frame, 80, 150)
            elif image_filter == BLUR:
                result = cv2.blur(frame, (13, 13))
            elif image_filter == FEATURES:
                result = frame
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners = cv2.goodFeaturesToTrack(frame_gray, 250, 0.01, 10)
                corners = np.int32(corners)
                for i in corners:
                    x, y = i.ravel()
                    cv2.circle(result, (x, y), 5, (0, 0, 155), 2)
            cv2.imshow(win_name, result)

            key = cv2.waitKey(1)
            if key == ord("Q") or key == ord("q") or key == 27:
                alive = False
            elif key == ord("C") or key == ord("c"):
                image_filter = CANNY
            elif key == ord("B") or key == ord("b"):
                image_filter = BLUR
            elif key == ord("F") or key == ord("f"):
                image_filter = FEATURES
            elif key == ord("P") or key == ord("p"):
                image_filter = PREVIEW


if __name__ == "__main__":
    lab4 = OpenCV_Camera_Video_Utils()
    while True:
        print("Menu:")
        print("1. Camera Access")
        print("2. Video Reader")
        print("3. Video Writer")
        print("4. Webcam Filter")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            lab4.CameraAccess()
        elif choice == "2":
            lab4.VideoReader("nature.mp4")
        elif choice == "3":
            lab4.VideoWriter()
        elif choice == "4":
            lab4.WebCamFilter()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")