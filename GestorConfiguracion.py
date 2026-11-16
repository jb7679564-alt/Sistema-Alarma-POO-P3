import json

# CLASE PARA GESTIONAR DATOS SENSIBLES DESDE JSON
class GestorConfiguracion:
    def __init__(self, ruta_archivo="config_secreta.json"):
        self.__ruta_archivo = ruta_archivo
        self.__datos = self.__cargar_configuracion()

    def __cargar_configuracion(self):
        # Carga el archivo JSON o usa valores por defecto si no existe
        try:
            with open(self.__ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return {
                "clave_maestra": "4321",
                "palabra_inicio": "inicio",
                "palabra_apagado": "desactivar",
                "max_intentos": 3,
                "tiempo_warning_seg": 5
            }

    def obtener_clave_maestra(self):
        return self.__datos.get("clave_maestra", "4321")

    def obtener_palabra_inicio(self):
        return self.__datos.get("palabra_inicio", "inicio")

    def obtener_palabra_apagado(self):
        return self.__datos.get("palabra_apagado", "desactivar")

    def obtener_max_intentos(self):
        return self.__datos.get("max_intentos", 3)

    def obtener_tiempo_warning(self):
        return self.__datos.get("tiempo_warning_seg", 5)