from django.http import HttpResponse
from django.shortcuts import render, redirect
from time import time
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import threading

from pygame import mixer

from gtts import gTTS 
import os 
import pyttsx3
import math
import json

from .yawn import *

import pyjokes
flagger=True
ear_data = []
yawn_data=[]
total_count=0
total_time = 0
# joke_counter = 0

def index(request):
    return render(request, 'home.html')
def errorImg(request):
    return render(request, 'error.html')


def alert_function():
    global joke_counter,total_count
    engine = pyttsx3.init()
    engine.say("Too much distraction , please stay aware")
    # if(joke_counter%5 == 0):
    #     engine.say((pyjokes.get_joke()))
    # else:
    #     joke_counter=joke_counter+1
    total_count=total_count+1
    engine.runAndWait()

def look_forward():
    global total_count
    total_count=total_count+1
    engine = pyttsx3.init()
    engine.say("Look Fordward , Alert , Alert")

    engine.runAndWait()


def wake_up():
    global total_count
    total_count=total_count+1
    engine = pyttsx3.init()
    engine.say("Alert , Alert , Alert")

    engine.runAndWait()

def yawn_alert_function():
    global  total_count
    total_count = total_count+1
    engine = pyttsx3.init()
    engine.say("Yawning Too Much, Alert, Alert, Here is a joke for you sir")
    engine.runAndWait()


def my_eyes(request):
    global ear_data
    global yawn_data

    def eye_aspect_ratio(eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    EYE_AR_THRESH = 0.20
    global flagger
    flagger = True 
    COUNTER = 0
    TOTAL = 0
    # cur_time=0
    diff=0
    sleepy_counter=0
    flag=0
    all_time=time.time()
    upper_counter=0
    lower_counter=0
    sum_ear=0
    yawn_all_time=time.time()
    yawn_counter=0
    tilt_counter=0

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
 
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    vs = VideoStream(src=0).start()
    yawns = 0
    yawn_status = False 

    engine = pyttsx3.init()
    engine.say("Initialization Begins, loading facial landmark predictor")
    engine.runAndWait()

    ear_data_time = time.time()
    ear_data_sum = 0
    ear_data_frames = 0
    temp_yawns=0
    0

    while flagger:
        flagger = True
        frame = vs.read()
        yawn_counter+=1

        frame = imutils.resize(frame, width=450)
        #YAWN
        image_landmarks, lip_distance = mouth_open(frame)
        prev_yawn_status = yawn_status
        output_text=''
        if(lip_distance > 13):
            yawn_status = True 
            cv2.putText(frame, "Subject is Yawning", (50,450), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),2)
            output_text = " Yawn Count: " + str(yawns + 1)

            cv2.putText(frame, output_text, (50,50),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)
        else:
            yawn_status = False 
        print(yawns)
        if prev_yawn_status == True and yawn_status == False:
            yawns += 1
            temp_yawns+=1
        #YAWN
        degree=0


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        tilt_flag=0
        shape=[]
        a=0
        b=0
        #Tilt Counter
        for (i, rect) in enumerate(rects):
            tilt_flag=1
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            (a,b)=shape[42:48][0]-shape[36:42][0]
        if(tilt_flag==0):
            tilt_counter+=1
            cv2.putText(frame, "Tilt Counter: {}".format(tilt_counter), (40, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
           
            if(tilt_counter == 10):
                a = threading.Thread(target=alert_function, name='Thread-a', daemon=True)
                a.start()
                tilt_counter = 0

           
        else:
            degree=math.degrees(math.atan(b/a))
            #tilt_counter = 0
        degree=abs(degree)
        print(degree)
        if(degree>20):
            tilt_counter+=1
            cv2.putText(frame, "Tilt_EYE Counter: {}".format(tilt_counter), (40, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            if(tilt_counter == 10):
                a = threading.Thread(target=look_forward, name='Thread-a', daemon=True)
                a.start()
                tilt_counter = 0
        else:
            if(degree!=0):
                tilt_counter=0



        #TILT

        rects = detector(gray, 0)
    
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
    
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
    
            ear = (leftEAR + rightEAR) / 2.0
    
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            
            
            # current_time=time.time()
            if(time.time()-all_time >=2):
                if(lower_counter >= upper_counter):
                    a = threading.Thread(target=wake_up, name='Thread-a', daemon=True)
                    a.start()
                lower_counter=0
                upper_counter=0 
                all_time=time.time()


            sum_ear+=ear   
            if(time.time() - yawn_all_time >=45):
                sum_ear=sum_ear/yawn_counter
                z=1/np.sqrt(np.exp(yawns))
                x=(sigmoid(sum_ear)*z)
                result = 1-(1/(1+(3)*x))
                if(result <= 0.5):
                    a = threading.Thread(target=yawn_alert_function, name='Thread-a', daemon=True)
                    a.start()
                
                sum_ear=0
                yawn_counter=0
                yawn_all_time=time.time()


            ear_data_sum += ear
            ear_data_frames += 1

            if(round(time.time() - ear_data_time) >= 10):
                ear_data.append(ear_data_sum/ear_data_frames)
                yawn_data.append(temp_yawns)
                ear_data_sum = 0
                ear_data_frames = 0
                temp_yawns=0
                ear_data_time = time.time()

            if ear < EYE_AR_THRESH:
                lower_counter=lower_counter+1
                # COUNTER += 1

    
            else:
                upper_counter+=1
                # cur_time = 0
                # if COUNTER >= EYE_AR_CONSEC_FRAMES:
                #     TOTAL += 1
    
                # COUNTER = 0
            # cv2.putText(frame, "Blink: {}".format(TOTAL), (10, 30),
            #     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, output_text, (50,50),
                    cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2) 
    

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
     
        if key == ord("q"):
            break

    cv2.destroyAllWindows()
    return redirect('/')


def leave(request):
    global flagger
    flagger = False
    cv2.destroyAllWindows()


    global ear_data
    global yawn_data

    timer = 10
    ear_dict = {}
    for ear in ear_data:
        ear_dict[timer] = ear
        timer+=10

    timer = 10
    yawn_dict = {}
    for yawn in yawn_data:
        yawn_dict[timer] = yawn
        timer += 10

    ear_data = []
    yawn_data = []

    return render(request, 'result.html',{
        'yawn_data':yawn_dict, 'ear_data':ear_dict,'total_count' : total_count,
        'data':json.dumps(
            {
                'yawn': yawn_dict,
                'ear': ear_dict
            }
        )
    })



def download_file(request):
    fh = request.POST['data']
    fh = json.loads(fh)

    filename = "data.json"
    response = HttpResponse(json.dumps(fh, indent=4), content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def presentation(request):
    return render(request, 'presentation.html')

def copy_my_eyes(request):
    return render(request, 'maps.html')

   

