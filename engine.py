import cv2
import numpy as np

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # تحسين التباين
    gray = cv2.equalizeHist(gray)

    # Blur لتقليل الضوضاء
    blur = cv2.GaussianBlur(gray, (7,7), 0)

    # كشف الحواف
    edges = cv2.Canny(blur, 40, 120)

    # تكبير الحواف
    kernel = np.ones((7,7), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=3)

    # استخراج الكونتور
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros_like(gray)

    if contours:
        largest = max(contours, key=cv2.contourArea)

        # تجاهل الأشياء الصغيرة
        if cv2.contourArea(largest) > 5000:
            cv2.drawContours(mask, [largest], -1, 255, thickness=cv2.FILLED)

    # تنعيم الماسك
    mask = cv2.GaussianBlur(mask, (41,41), 0)
    mask = mask / 255.0
    mask = np.expand_dims(mask, axis=2)

    # تعتيم الخلفية
    dark = frame * 0.2

    # Glow احترافي
    glow = np.zeros_like(frame)
    glow[:,:,1] = edges
    glow = cv2.GaussianBlur(glow, (35,35), 0)

    # Outline إضافي
    outline = cv2.Canny(mask[:,:,0].astype(np.uint8)*255, 100, 200)
    outline = cv2.dilate(outline, np.ones((3,3),np.uint8), iterations=1)

    outline_color = np.zeros_like(frame)
    outline_color[:,:,1] = outline * 255

    # دمج
    result = frame * mask + dark * (1 - mask)
    result = cv2.addWeighted(result.astype(np.uint8), 1, glow, 0.9, 0)
    result = cv2.addWeighted(result, 1, outline_color, 0.7, 0)

    return result.astype(np.uint8)
