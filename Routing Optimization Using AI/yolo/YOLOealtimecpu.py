import cv2
import numpy as np
import time
# Load Yolo object detector 
net = cv2.dnn.readNet("C:/Users/piyus/Downloads/yolo/yolov3.weights", "C:/Users/piyus/Downloads/yolo/yolov3.cfg")
classes = []
iti=0
with open("C:/Users/piyus/Downloads/yolo/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))  # to get list of colors for each possible class
# Loading video
cap = cv2.VideoCapture(0)
startingtime = time.time()
frame_id = 0
while True:
    _, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing information on the screen
    class_ids = []
    confidences = []
    boxes = []  # coordinate of bounding box
    for out in outs:
        for detection in out:
            scores = detection[5:]  # getting all 80 scores
            class_id = np.argmax(scores)  # finding the max score
            confidence = scores[class_id]
            # find out strong predictions greater then. 5
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #print(label,"=",i)
    count_label = []
    count = []
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if label not in count_label :
                count_label.append(label)
                count.append(int(1))
            else :
                tmp = 0
                for k in count_label :
                    if k == label :
                        count[tmp] = count[tmp]+1
                    tmp = tmp+1
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 3, color, 3)
    iti= iti+1
    print("ITERATION =", iti)
    for k in range(len(count_label)):
        print(count_label[k],"=",count[k])

    elapsed_time = time.time()-startingtime
    fps = frame_id/elapsed_time
    cv2.putText(frame, "FPS:"+str(fps), (10, 30), font, 3, (0, 0, 0), 1)
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)  # 0 keeps on hold 1 waits for a millisecond
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
