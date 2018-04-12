from channels.generic.websocket import WebsocketConsumer
import json
import serial
from .models import scheduler


class SerialConsumer(WebsocketConsumer):

    _puerto='/dev/ttyACM0'
    __job_enviar= scheduler
    
    __ser = serial.Serial(_puerto, 9600)
    __ser.is_open

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def connect(self):
        self.__job_enviar.add_job(self.enviar, 'interval', seconds=0.1, id='job_enviar')
        self.accept()

    def disconnect(self, close_code):
        self.__job_enviar.remove_job('job_enviar')
        print("job_enviar removido")
        __ser.close()

    def receive(self, text_data):
        json_dic = json.loads(text_data)
        instruccion = json_dic['tipo']
        
        
        if instruccion == 'start':
            self.__job_enviar.resume_job('job_enviar')
            print("starteeed")
        elif instruccion == 'stop':
            print("stopeddd")
            self.__job_enviar.pause_job('job_enviar')
        elif instruccion == 'baudio':
            baudios = json_dic['baudios']
            self.__ser = serial.Serial(self._puerto, baudios)


    def enviar(self):
        self.send(text_data=json.dumps({
            'message': str(self.__ser.readline())
            }))
