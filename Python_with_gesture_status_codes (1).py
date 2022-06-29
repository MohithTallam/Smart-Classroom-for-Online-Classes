
""" Nokia Project - Team 1 : Smart IoT based Online Class System
    python version 3.9
    mediapipe version 0.8.8 
    opencv version 4.5.3.56
    pyserial version 3.5
    numpy version 1.19.3   """

import cv2                    # Use Opencv for extracting video from the camera and manipulation.                     
import mediapipe as mp        # We use mediapipe to extract the keypoints(coordinates) of the subject(teacher). 
import numpy as np            # Processing the frame of the video as a RGB array.
import serial                 # Communication with any serial device which will control the servo motors.


ser=serial.Serial('COM4',9600,timeout=.1)                           #initialize serial object of arduino on COM3 at 9600 baudrate with a timeout interval of 0.1

def zoom(x,image,scale):  
    height, width, channels = image.shape                           # get the webcam resolution
    
    centerX,centerY=int(height/2),int(width/2)                      # Finding the center co-ordinates of the frame.
    radiusX,radiusY = int(centerX*scale), int(centerY*scale)        # To find the region which has to be cropped from the center.

    minX,maxX=centerX-radiusX,centerX+radiusX                       # maxX and maxY are the highest co-ordinate value of the edge of the transformed frame.
    minY,maxY=centerY-radiusY,centerY+radiusY                       # minX and minY are the lowest co-ordinate value of the transformed frame.

    cropped = image[minX:maxX, minY:maxY]                           # In order to zoom into the frame we crop to the min and max values defined earlier.
    resized_cropped = cv2.resize(cropped, (width, height))          # Calculates the newly transformed image.
    
    if(x=='1'):                                                     # When status code received is 1 the program will zoom in the video by decreasing the scaling factor by 0.2.
        scale -= 0.2  
        if(scale <=1.2):                                            # 1.2 is the minimum allowed scaling factor for Zoom In.
            scale = 1.2
        #print(scale)

    elif(x=='2'):                                                  # When status code received is 2 the program will zoom out the video by increasing the scaling factor by 0.2.
        scale += 0.2  
        if(scale >=3.2):                                           # 3.2 is the maxium allowed scaling factor for Zoom Out.
            scale = 3.2
        #print(scale)
    return(resized_cropped,scale)

def pausePlay(x):
    if(x=='3'):                                                          # status code received is 3 then pause and if status code 4 is received then play
        while(x!='4'):
            x=str((ser.read()),'UTF-8')
            pass

mp_drawing = mp.solutions.drawing_utils                                  # mp.solutions.drawing_utils and mp.solutions.drawing_styles are mediapipe functions for drawing the keypoints on the video.  
mp_drawing_styles = mp.solutions.drawing_styles                          
mp_pose = mp.solutions.pose                                              # mp.solutions.pose  is a mediapipe function for extracting the keypoints from each  frame of the video.                                           # instanciate a serial object, with USB port connected to arduino 'COM3' at baud rate of 9600
scale=3.2
while True:
    try:
        scale=3.2                                                            # We use try and except statements to handle errors.
        cap = cv2.VideoCapture(1)                                            # cv2.VideoCapture(1)  is a function which takes in number as an arugument(number signifies the webcam) and returns the capture object(cap).
        print("width:",cap.get(3),"height",cap.get(4),"fps:",cap.get(5))     # cap.get() is used to get the webcam parameters like resolution and frame rate.
        
        """MIN_DETECTION_CONFIDENCE: Minimum confidence value ([0.0, 1.0]) from the person-detection model for the detection to be considered successful.
          MIN_TRACKING_CONFIDENCE: Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the pose landmarks to be considered tracked successfully.
          Landmark is the points extracted from the pose estimation model"""

        with mp_pose.Pose(
            min_detection_confidence=0.1,             
            min_tracking_confidence=0.1) as pose:

          while cap.isOpened():                                               # We run a while loop until the capture object(cap) returns that the camera is open.   
            success, image = cap.read()                                       # cap.read() to read the video from the capture object.
            if not success:
              print("Ignoring empty camera frame.")
              continue
            
            statusRecv=str((ser.read()),'UTF-8')                              # read the data from the serial interface through ser.read(), which reutrns byte values from the Arduino, convert them back to strings
            print(statusRecv)                                                 # print gesture code received for debugging.
            
            image,scale=zoom(statusRecv,image,scale)                          # Calling the zoom function
            pausePlay(statusRecv)                                             # Calling the pause and play function
            
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)       # cv2.flip() we use this function to flip the inverted image.
                                                                              # cv2.cvtColor() we use this function to convert the color space to 'BGR2RGB'. 
            image.flags.writeable = False                                     # we set the frame to read only to enhance the performance of the code.
            results = pose.process(image)                                     # pose.process() extracts the keypoints from the frame.
            image.flags.writeable = True                                      # since we have finished processing we set the frame back to read and write so that we can draw the keypoints.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)                    # we revert back to the original colour space.

## mp_drawing.draw_landmarks() takes in input as the frame, results and mediapipe functions to draw keypoints on the frame,uncomment if you want to see the points on the video comment 

    ##        mp_drawing.draw_landmarks(                                      
    ##            image,
    ##            results.pose_landmarks,
    ##            mp_pose.POSE_CONNECTIONS,
    ##            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    
            
            """We extract the left and right shoulder coordinates from the results list and multiply it by frame width and height to convert the coordinates(which were returned
               normalized in the range[0.0,1.0]) back to the original resolution values.
               Since we want the center of our subject to fit within the frame, we define the center of the subject as the center of their shoulders, hence we add
               the left and right shoulders coordinates and divide it by two."""

            image_height, image_width, _ = image.shape
            center_x=results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width + results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width
            center_x = center_x /2
            center_y=results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height + results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height 
            center_y=center_y /2

            print("center_x:",center_x,"center_y:",center_y)
            print("------------------------------------------------------") # Debugging information, center of the person wrt shoulders.
            
            cv2.imshow('Tracked video', image)                              # cv2.imshow() is used to display the video in a window.

            if(center_x<(image_width/4)):                                   # Control the servos with status codes on where to move. ser.write() sends bytes through serial communication in UTF-8 format.
                #print('1')
                ser.write(bytes('1', 'utf-8'))                              # Position irl right, position video left => move servo left.                             
            elif(center_x>image_width - (image_width/4)):
                #print('2')
                ser.write(bytes('2', 'utf-8'))                              # Position irl left, position video right => move servo right.                          
            else:
                #print('0')
                ser.write(bytes('0','utf-8'))                               # Stop the motion as the subject is in center of the frame.
                
            if cv2.waitKey(5) & 0xFF == 27:                                 # This part of the code is used to terminate the program (27 = esc on our keyboard).
              break
              cap.release()

    except:
        scale=3.2                                                           # incase zooming causes pose extraction to fail
        pass
