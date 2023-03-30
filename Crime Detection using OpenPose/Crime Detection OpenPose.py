# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--thr', default=0.10, type=float, help='Threshold value for pose parts heat map')
parser.add_argument('--width', default=368, type=int, help='Resize input to specific width.')
parser.add_argument('--height', default=368, type=int, help='Resize input to specific height.')

args = parser.parse_args()

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

inWidth = args.width
inHeight = args.height

net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

cap = cv.VideoCapture(args.input if args.input else 0)

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    
    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > args.thr else None)
    #punch detection
    punch=False
    """in Second phase ie multiperson detection 
        for i in (people[i]!=None):
            #single person code here
            """
    if (points[0] != None):
        if (points[4] != None and points[7] != None):
            if (abs(points[0][0] - points[4][0] ) > 4 *abs(points[0][1] - points[1][1] ) or abs(points[0][0] - points[7][0]) > 4 *abs(points[0][1] - points[1][1] )):
                punch=True
    if punch:
        print("punch detected ")
        print("dist Rwrist-nose ",abs(points[0][0] - points[4][0] ) ,"dist Lwrist-nose "  , abs(points[0][0] - points[7][0]) ,"dist 4*neck-nose ", 4*abs(points[0][1] - points[1][1] ))

        
    #kick detection
    kick=False
    """in Second phase ie multiperson detection 
        for i in (people[i]!=None):
            #single person code here
            """
    if (points[0] != None):
        if (points[10] != None and points[13] != None):
            if (abs(points[0][0] - points[10][0] ) > 3* abs(points[0][1] - points[1][1] ) or abs(points[0][0] - points[13][0]) > 3*abs(points[0][1] - points[1][1] )):
                kick=True
    if kick:
        print("kick detected")
        print("dist RAnkle-nose ",abs(points[0][0] - points[10][0] ) ,"dist LAnkle-nose "  , abs(points[0][0] - points[13][0]) ,"dist 3*neck-nose ", abs(points[0][1] - points[1][1] ))
    
    
    #fall detection
    fall=False
    """in Second phase ie multiperson detection 
    for i in (people[i]!=None):
        #single person code here
        """
    if (points[0] != None):
        if (points[9] != None and points[12] != None):
            x=abs(points[0][0]-abs(points[9][0] + points[12][0])/2)
            y=abs(points[0][0]-
                  abs(points[9][1] +
                      points[12][1])/2)-points[1][1]
            if(y!=0):
                if (x/y > 1):
                    print("fall detected")
                    fall=True
    
    """in Second phase ie multiperson detection 
        for i in (people[i]!=None):
            #single person code here
            """

    if(fall and (punch or kick)):
        print("____________________________________________________________________________________________")
        print("crime detected")
        print("____________________________________________________________________________________________")
        punch =False
        kick = False
        fall = False
        

    
    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0))

    cv.imshow('OpenPose using OpenCV', frame)
