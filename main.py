import cv2
from object_detection import ObjectDetection
import object_tracking
import driving_analysis
import frame_perspective
import math
import time

start_time = time.time()

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture('input_videos/los_angeles.mp4')
out = cv2.VideoWriter('output_videos/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (1920, 1080))

params = object_tracking.VehiclesParameters()

current_frame = 0

while cap.isOpened():
    current_frame += 1
    ret, frame = cap.read()
    transformedFrame = frame_perspective.transform(frame)
    if not ret:
        break

    # Point current frame
    current_point = []

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(transformedFrame)

    for box in boxes:
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        current_point.append((cx, cy))
        cv2.rectangle(transformedFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    tracking_objects_copy = params.tracking_objects.copy()
    xy_point_cur_copy = current_point.copy()
    for object_id, pt2 in tracking_objects_copy.items():
        object_exists = False
        for pt in xy_point_cur_copy:
            distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
            if distance > 40 and pt[0] - 100 < pt2[0] < pt[0] + 100 and pt[1] > pt2[1]:
                params.vehicles_distance[object_id] = int(distance / 75)
            if distance < 40:
                params.vehicles_frames[object_id] += 1
                params.pixelsPerFrame[object_id] += int(distance)
                params.vehicles_speed_cur[object_id] = int(params.pixelsPerFrame[object_id] /
                                                           params.vehicles_frames[object_id] * 24 / 6)
                params.vehicles_acceleration[object_id] = params.vehicles_speed_cur[object_id] - \
                                                          params.vehicles_speed_prev[object_id]
                params.vehicles_speed_prev[object_id] = params.vehicles_speed_cur[object_id]
                params.vehicles_rating[object_id] = driving_analysis.analysis(params.vehicles_distance[object_id],
                                                                              params.vehicles_speed_cur[object_id],
                                                                              params.vehicles_acceleration[object_id])
                params.tracking_objects[object_id] = pt
                object_exists = True
                if pt in current_point:
                    current_point.remove(pt)
                continue

        # Remove IDs lost
        if not object_exists:
            params.remove_vehicle(object_id)

    # Add new IDs found
    params.add_new_vehicle(params.track_id, current_point)

    for object_id, pt in params.tracking_objects.items():
        cv2.putText(transformedFrame, str(params.vehicles_rating[object_id]), (pt[0] - 80, pt[1] - 40), 0, 1,
                    (0, 0, 255), 3)
        cv2.putText(transformedFrame, 'acc ' + str(params.vehicles_acceleration[object_id]) + ' m/s',
                    (pt[0] - 80, pt[1] - 130), 0, 1,
                    (0, 205, 0), 3)
        cv2.putText(transformedFrame, 'dist ' + str(params.vehicles_distance[object_id]) + ' m', (pt[0] - 80, pt[1] - 100), 0,
                    1,
                    (0, 205, 0), 3)
        cv2.putText(transformedFrame, 'spd ' + str(params.vehicles_speed_cur[object_id]) + ' km/h', (pt[0] - 80, pt[1] - 70),
                    0, 1,
                    (0, 205, 0), 3)
        cv2.putText(transformedFrame, 'car ' + str(object_id), (pt[0] - 80, pt[1]), 0, 1, (255, 0, 0), 3)

    final_frame = frame_perspective.cancel_transform(transformedFrame, frame)
    out.write(final_frame)
    cv2.imshow("Aggressive driving analysis", final_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
