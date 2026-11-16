# CLASE SENSOR DE MOVIMIENTO
class SensorMovimiento:
    def __init__(self, zona="Entrada Principal", sensibilidad="Alta"):
        self.__zona = zona
        self.__sensibilidad = sensibilidad
        self.__deteccion_activa = False

    def consultar_zona(self):
        return self.__zona

    def consultar_sensibilidad(self):
        return self.__sensibilidad

    def cambiar_sensibilidad(self, nueva_sensibilidad):
        self.__sensibilidad = nueva_sensibilidad

    def activar_sensor(self):
        self.__deteccion_activa = True
        return f"Sensor en [{self.__zona}] (Sensibilidad: {self.__sensibilidad}) ACTIVADO."

    def desactivar_sensor(self):
        self.__deteccion_activa = False
        return f"Sensor en [{self.__zona}] DESACTIVADO."

    def detectar(self):
        if not self.__deteccion_activa:
            return False, "Sensor inactivo."
        return True, f"⚠️ ¡MOVIMIENTO DETECTADO EN {self.__zona.upper()}!"