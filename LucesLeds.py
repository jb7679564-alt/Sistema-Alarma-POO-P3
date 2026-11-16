from DispositivoNotificacion import DispositivoNotificacion

# CLASE HIJA 2 (Herencia y Polimorfismo)
class LucesLeds(DispositivoNotificacion):
    def __init__(self, nombre, color="Rojo"):
        super().__init__(nombre)
        self.__color = color
        self.__modo_parpadeo = "Intermitente Rápido"

    # Polimorfismo: retorna alerta lumínica para la consola gráfica
    def notificar(self, mensaje):
        if self.consultar_estado():
            return f"🚨 LUCES {self.__color.upper()} ({self.__modo_parpadeo}): {mensaje}"
        return "Las luces están apagadas."

    def cambiar_color(self, nuevo_color):
        self.__color = nuevo_color