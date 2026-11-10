from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from .camera import VideoCamera
from .models import Recurso  # Importamos la tabla de la base de datos

@login_required
def index(request):
    return render(request, 'detector/index.html')

@login_required
def inventario(request):
    # Traemos todos los equipos de la base de datos y contamos su estado
    recursos = Recurso.objects.all()
    total = recursos.count()
    disponibles = recursos.filter(estado='DISPONIBLE').count()
    
    return render(request, 'detector/inventario.html', {
        'recursos': recursos, 
        'total': total, 
        'disponibles': disponibles
    })
def gen(camera):
    # Generador que lee los frames de OpenCV infinitamente
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    # Ruta que transmite el flujo de video al tag <img> en HTML
    return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')