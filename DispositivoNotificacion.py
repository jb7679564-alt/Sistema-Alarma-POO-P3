# CLASE PADRE BASE
class DispositivoNotificacion:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__estado = False

    def consultar_nombre(self):
        return self.__nombre

    def consultar_estado(self):
        return self.__estado

    def encender(self):
        self.__estado = True
        return f"[{self.__nombre}] Dispositivo encendido."

    def apagar(self):
        self.__estado = False
        return f"[{self.__nombre}] Dispositivo apagado."

    # Método polimórfico base
    def notificar(self, mensaje):
        return f"[{self.__nombre}] Alerta general: {mensaje}"