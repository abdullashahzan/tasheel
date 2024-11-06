import cv2

def play_sample():
    # change to ip address when connected with ESP32
    video_path = '/home/shahzan/Documents/Codes/Django/tasheel/main/test_videos/Hajj 2023 Short video .mp4'  # Replace with the path to your video file

    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    # Loop through the video frames
    while True:
        ret, frame = cap.read()  # Read a single frame

        # Break the loop if there are no more frames
        if not ret:
            break

        # Display the frame
        cv2.imshow('Video Playback', frame)

        # Wait for 25 milliseconds; exit if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
