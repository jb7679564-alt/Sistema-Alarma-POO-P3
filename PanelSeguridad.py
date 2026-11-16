from GestorConfiguracion import GestorConfiguracion

# CLASE NÚCLEO DEL SISTEMA DE SEGURIDAD
class PanelSeguridad:
    def __init__(self):
        self.__config = GestorConfiguracion()
        self.__clave_correcta = self.__config.obtener_clave_maestra()
        self.__palabra_inicio = self.__config.obtener_palabra_inicio()
        self.__palabra_apagado = self.__config.obtener_palabra_apagado()
        self.__max_intentos = self.__config.obtener_max_intentos()
        self.__intentos_fallidos = 0
        # Estados posibles: APAGADO, INICIO, WARNING, ALARM
        self.__estado_sistema = "APAGADO"

    def consultar_estado(self):
        return self.__estado_sistema

    def consultar_intentos(self):
        return self.__intentos_fallidos

    def obtener_tiempo_warning(self):
        return self.__config.obtener_tiempo_warning()

    def verificar_comando_inicio(self, texto):
        return texto.strip().lower() == self.__palabra_inicio.lower()

    def verificar_comando_apagado(self, texto):
        return texto.strip().lower() == self.__palabra_apagado.lower()

    def armar_sistema(self):
        self.__estado_sistema = "INICIO"
        self.__intentos_fallidos = 0

    def activar_advertencia(self):
        self.__estado_sistema = "WARNING"
        self.__intentos_fallidos = 0

    def disparar_alarma_robo(self):
        self.__estado_sistema = "ALARM"

    def apagar_sistema(self):
        self.__estado_sistema = "APAGADO"
        self.__intentos_fallidos = 0

    def verificar_clave(self, clave_ingresada):
        clave = clave_ingresada.strip()
        if len(clave) != 4 or not clave.isdigit():
            raise ValueError("La clave debe tener exactamente 4 dígitos numéricos.")

        if clave == self.__clave_correcta:
            self.__intentos_fallidos = 0
            self.apagar_sistema()
            return True
        else:
            self.__intentos_fallidos += 1
            restantes = self.__max_intentos - self.__intentos_fallidos
            if self.__intentos_fallidos >= self.__max_intentos:
                self.disparar_alarma_robo()
                raise RuntimeError("¡LÍMITE DE 3 INTENTOS SUPERADO! POSIBLE ROBO DETECTADO.")
            raise PermissionError(f"Clave incorrecta. Intentos restantes: {restantes}")