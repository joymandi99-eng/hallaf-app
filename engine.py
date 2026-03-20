import cv2
import numpy as np

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    edges = cv2.Canny(blur, 50, 150)

    kernel = np.ones((5,5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=2)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(gray)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        cv2.drawContours(mask, [largest], -1, 255, thickness=cv2.FILLED)

    mask = cv2.GaussianBlur(mask, (31,31), 0)
    mask = mask / 255.0
    mask = np.expand_dims(mask, axis=2)

    dark = frame * 0.25

    glow = np.zeros_like(frame)
    glow[:,:,1] = edges
    glow = cv2.GaussianBlur(glow, (25,25), 0)

    result = frame * mask + dark * (1 - mask)
    result = cv2.addWeighted(result.astype(np.uint8), 1, glow, 0.8, 0)

    return result.astype(np.uint8)
