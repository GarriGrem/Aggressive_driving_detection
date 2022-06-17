import numpy as np
import cv2

width, height = 1920, 1080
pts1 = np.float32([[581, 499], [1018, 483], [135, 1039], [1630, 934]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])


def transform(frame):
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_frame = cv2.warpPerspective(frame, matrix, (width, height))
    return transformed_frame


def cancel_transform(transformed_frame, frame):
    matrix_cancel = cv2.getPerspectiveTransform(pts2, pts1)
    transformedFrame_cancel = cv2.warpPerspective(transformed_frame, matrix_cancel, (width, height))
    final_frame = cv2.addWeighted(frame, 0.5, transformedFrame_cancel, 1, 0)
    return final_frame
