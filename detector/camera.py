import cv2
import numpy as np
import os
import urllib.request

class VideoCamera(object):
    def __init__(self):
        # Asegúrate de mantener el 0, 1, o la URL que usas para encender tu cámara
        self.video = cv2.VideoCapture(0) 
        
        # 1. Definimos la ruta donde debería estar el archivo XML (en tu carpeta 'detector')
        current_dir = os.path.dirname(__file__)
        xml_path = os.path.join(current_dir, 'haarcascade_frontalface_default.xml')
        
        # 2. Si el archivo NO existe, Python lo descarga automáticamente del repositorio de OpenCV
        if not os.path.exists(xml_path):
            print("Descargando el modelo de rostros de OpenCV. Por favor espera...")
            url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
            urllib.request.urlretrieve(url, xml_path)
            print("¡Descarga de modelo completada!")

        # 3. Cargamos el modelo desde nuestro archivo local seguro
        self.face_cascade = cv2.CascadeClassifier(xml_path)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        
        if not success:
            frame_error = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame_error, "ERROR: SIN SENAL DE CAMARA", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, jpeg = cv2.imencode('.jpg', frame_error)
            return jpeg.tobytes()

        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detección de rostros
        rostros = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        
        conteo = len(rostros)
        for (x, y, w, h) in rostros:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        texto = f'Personas detectadas: {conteo}'
        cv2.putText(frame, texto, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()