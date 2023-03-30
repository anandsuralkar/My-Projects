# To use Inference Engine backend, specify location of plugins:
# export LD_LIBRARY_PATH=/opt/intel/deeplearning_deploymenttoolkit/deployment_tools/external/mklml_lnx/lib:$LD_LIBRARY_PATH
import cv2 as cv
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Path to image or video. Skip to capture frames from camera')
parser.add_argument('--thr', default=0.2, type=float, help='Threshold value for pose parts heat map')
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
ymax = 0
yavg = 0
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
        
        #print(points)


    l = [2,3,5,6]
    upperbody = True
    for i in l:
        if points[i] == None :
            upperbody = False
    punch=False
    if upperbody:
        #if ((points[0][1] - (points[9][1] + points[12][1]) / 2) < 10):
            #print("fall detected")
            #fall=True
        #punch detection
        punch=False

        dx =abs(points[2][0] - points[3][0])
        dy =abs(points[2][1] - points[3][1])
        dx2=abs(points[5][0] - points[6][0])
        dy2=abs(points[5][1] - points[6][1])
        
        
        try:
            if dy != 0:
                #print(dx,dy,dx/dy)
                if dx/dy >1:
                    punch=True
            if dy2 != 0:
                #print(dx2,dy2,dx2/dy2)
                if dx2/dy2 >1:
                    punch=True
            if punch:
                print("punch or stab detected")
        except:
            pass
    kick = False
        #kick detection
    l = [8,9,11,12]
    lowerbody = True
    for i in l:
        if points[i] == None :
            lowerbody = False
    if lowerbody:
        dx =abs(points[8][0] - points[9][0])
        dy =abs(points[8][1] - points[9][1])
        dx2=abs(points[11][0] - points[12][0])
        dy2=abs(points[11][1] - points[12][1])
        #print(dx,dy,dx/dy)
        #print(dx2,dy2,dx2/dy2)
        try:
            if dy != 0:
                if dx/dy >0.9:
                    kick=True
            if dy2 != 0:
                if dx2/dy2 >0.9:
                    kick=True
            if kick:
                print("kick detected")
        except:
            pass
        #kick detection
        kick=False

    fall=False
    #fall detection
    if ymax < yavg :
        ymax = yavg
    if upperbody and points[8] != None and points[11] != None and points[0] != None:
        x1 = (points[2][0] + points[5][0])/2
        y1 = points[0][1]
        xi = points[2][0]
        xj = points[5][0]
        xx = abs(xj - xi)
        x2 = (points[8][0] + points[11][0])/2
        y2 = (points[8][1] + points[11][1])/2

        yavg = (y1+y2) / 2
        dx = x2 - x1
        dy = y2 - y1
        #print(dx,dy,dx/dy)
        if dy != 0:
            if abs(dx/dy) > 1:
                fall = True
        #print(ymax,yavg,xx/2)
        if (ymax - yavg) > xx/2 :
            fall = True
            print("fall detected")
        if(fall and punch or kick):
            print("crime detected")
    punch=False
    fall=False
    kick=False
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
