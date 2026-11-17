from AlarmaBocina import AlarmaBocina
from LucesLeds import LucesLeds
from SensorMovimiento import SensorMovimiento
from PanelSeguridad import PanelSeguridad
from UsuarioAutorizado import UsuarioAutorizado
from BackendExcel import BackendExcel

# CLASE CONTROLADOR (UNE LÓGICA DEL SISTEMA, POLIMORFISMO Y EXCEL)
class ControladorAlarma:
    def __init__(self):
        self.__panel = PanelSeguridad()
        self.__sensor = SensorMovimiento(zona="Entrada Principal", sensibilidad="Alta")
        self.__bocina = AlarmaBocina("Sirena Principal", volumen_db=110)
        self.__luces = LucesLeds("Estrobo Emergencia", color="Rojo")
        self.__dispositivos = [self.__bocina, self.__luces]

        self.__backend_excel = BackendExcel("BaseDatosAlarma.xlsx")
        self.__usuario_activo = None
        self.__modo_silencioso = False

    def obtener_backend_excel(self):
        return self.__backend_excel

    def consultar_estado_actual(self):
        return self.__panel.consultar_estado()

    def obtener_tiempo_warning(self):
        return self.__panel.obtener_tiempo_warning()

    def obtener_nombre_operador(self):
        if self.__usuario_activo is not None:
            return self.__usuario_activo.consultar_nombre()
        return "Sin Operador"

    def configurar_operador(self, nombre, tipo_doc, num_doc):
        # Crea y valida el usuario; si falla lanza ValueError hacia la interfaz
        usuario = UsuarioAutorizado(nombre, tipo_doc, num_doc)
        self.__usuario_activo = usuario
        self.__backend_excel.registrar_usuario(usuario)
        self.__backend_excel.registrar_evento(
            usuario.consultar_nombre(),
            self.__panel.consultar_estado(),
            f"Operador registrado ({tipo_doc}: {num_doc})"
        )
        return f"✅ Operador activo: {usuario.consultar_nombre()} ({tipo_doc} - {num_doc})"

    def cambiar_sensibilidad(self, nueva_sensibilidad):
        self.__sensor.cambiar_sensibilidad(nueva_sensibilidad)
        return f"⚙️ Sensibilidad del sensor ajustada a: {nueva_sensibilidad}"

    def cambiar_modo_silencioso(self, silencioso):
        self.__modo_silencioso = silencioso
        estado_txt = "ACTIVADO (Solo luces)" if silencioso else "DESACTIVADO (Bocina + Luces)"
        return f"🔇 Modo silencioso: {estado_txt}"

    def simular_deteccion_movimiento(self):
        if self.__panel.consultar_estado() != "INICIO":
            return False, "⚠️ La alarma debe estar armada (en estado INICIO) para detectar movimiento."

        detectado, msg_sensor = self.__sensor.detectar()
        if detectado:
            self.__panel.activar_advertencia()
            tiempo = self.__panel.obtener_tiempo_warning()
            self.__backend_excel.registrar_evento(
                self.obtener_nombre_operador(),
                "WARNING",
                "Movimiento detectado en sensor PIR. Esperando clave."
            )
            return True, (
                f"{msg_sensor}\n"
                f"⏳ ESTADO WARNING: Tiene {tiempo} segundos o 3 intentos para ingresar su clave de 4 dígitos."
            )
        return False, msg_sensor

    def disparar_robo_por_tiempo(self):
        if self.__panel.consultar_estado() == "WARNING":
            self.__panel.disparar_alarma_robo()
            mensajes = ["⏰ ¡TIEMPO AGOTADO! POSIBLE ROBO EN CURSO."]
            mensajes.extend(self.__activar_dispositivos_alerta("INTRUSIÓN CONFIRMADA"))
            self.__backend_excel.registrar_evento(
                self.obtener_nombre_operador(),
                "ALARM",
                "Alarma disparada por tiempo límite agotado."
            )
            return True, "\n".join(mensajes)
        return False, ""

    def __activar_dispositivos_alerta(self, motivo):
        salidas = []
        for disp in self.__dispositivos:
            if self.__modo_silencioso and isinstance(disp, AlarmaBocina):
                salidas.append("🔇 Bocina silenciada por configuración del operador.")
                continue
            disp.encender()
            # Polimorfismo en acción
            salidas.append(disp.notificar(motivo))
        return salidas

    def __apagar_todos_dispositivos(self):
        for disp in self.__dispositivos:
            disp.apagar()
        self.__sensor.desactivar_sensor()

    def procesar_comando_consola(self, texto_ingresado):
        comando = texto_ingresado.strip()
        estado = self.__panel.consultar_estado()

        if not comando:
            return ["⚠️ Ingrese un comando o clave válida."]

        # Validar que haya un operador registrado antes de armar la alarma
        if self.__usuario_activo is None:
            return ["❌ Error: Primero registre un Operador (Nombre y Documento) en la barra superior."]

        # CASO 1: SISTEMA APAGADO -> Espera palabra clave 'inicio'
        if estado == "APAGADO":
            if self.__panel.verificar_comando_inicio(comando):
                self.__panel.armar_sistema()
                msg_sensor = self.__sensor.activar_sensor()
                self.__backend_excel.registrar_evento(
                    self.obtener_nombre_operador(),
                    "INICIO",
                    "Alarma armada mediante comando 'inicio'."
                )
                return [
                    "🟢 SISTEMA ARMADO (ESTADO INICIO): Vigilancia activa.",
                    f"   {msg_sensor}",
                    "   (Presione 'Simular Movimiento PIR' para probar una intrusión)."
                ]
            else:
                return ["ℹ️ La casa es segura y la alarma está apagada. Escriba 'inicio' para armar."]

        # CASO 2: SISTEMA EN INICIO (ARMADO) -> Espera movimiento
        elif estado == "INICIO":
            return ["🛡️ Sistema vigilando. Si desea probar intrusión, pulse 'Simular Movimiento PIR'."]

        # CASO 3: SISTEMA EN WARNING -> Espera clave numérica de 4 dígitos
        elif estado == "WARNING":
            try:
                if self.__panel.verificar_clave(comando):
                    self.__apagar_todos_dispositivos()
                    self.__backend_excel.registrar_evento(
                        self.obtener_nombre_operador(),
                        "APAGADO",
                        "Clave correcta ingresada. Alarma desactivada."
                    )
                    return ["✅ CLAVE CORRECTA. Identidad validada. Sistema desactivado de forma segura."]
            except ValueError as e:
                return [f"⚠️ Error de formato: {e}"]
            except PermissionError as e:
                self.__backend_excel.registrar_evento(
                    self.obtener_nombre_operador(),
                    "WARNING",
                    f"Intento fallido de clave ({e})."
                )
                return [f"❌ {e}"]
            except RuntimeError as e:
                mensajes = [f"🚨 {e}"]
                mensajes.extend(self.__activar_dispositivos_alerta("3 INTENTOS FALLIDOS"))
                mensajes.append("🔑 Para detener la sirena ingrese la palabra maestra de desactivación.")
                self.__backend_excel.registrar_evento(
                    self.obtener_nombre_operador(),
                    "ALARM",
                    "Alarma disparada tras superar 3 intentos fallidos."
                )
                return mensajes

        # CASO 4: SISTEMA EN ALARM (ROBO) -> Exige palabra clave 'desactivar'
        elif estado == "ALARM":
            if self.__panel.verificar_comando_apagado(comando):
                self.__panel.apagar_sistema()
                self.__apagar_todos_dispositivos()
                self.__backend_excel.registrar_evento(
                    self.obtener_nombre_operador(),
                    "APAGADO",
                    "Alarma de robo restablecida mediante palabra maestra."
                )
                return ["🔒 ALARMA DETENIDA Y RESTABLECIDA. El sistema regresó a estado APAGADO."]
            else:
                return ["🚨 ¡ALERTA DE ROBO ACTIVA! Ingrese la palabra maestra exacta para apagar."]

        return ["Estado desconocido."]