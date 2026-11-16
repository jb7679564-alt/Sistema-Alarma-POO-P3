from DispositivoNotificacion import DispositivoNotificacion

# CLASE HIJA 1 (Herencia y Polimorfismo)
class AlarmaBocina(DispositivoNotificacion):
    def __init__(self, nombre, volumen_db=110):
        super().__init__(nombre)
        self.__volumen_db = volumen_db
        self.__tono = "Sirena Policial"

    # Polimorfismo: retorna texto formateado para la consola gráfica
    def notificar(self, mensaje):
        if self.consultar_estado():
            return f"📢 BOCINA ({self.__volumen_db} dB - {self.__tono}): {mensaje}"
        return "La bocina está apagada."

    def cambiar_volumen(self, nuevo_volumen):
        if nuevo_volumen < 0 or nuevo_volumen > 120:
            raise ValueError("El volumen debe estar entre 0 y 120 dB.")
        self.__volumen_db = nuevo_volumen