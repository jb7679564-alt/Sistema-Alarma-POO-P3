from datetime import datetime
from openpyxl import Workbook, load_workbook

# CLASE BACKEND PARA ALMACENAMIENTO PERSISTENTE EN EXCEL
class BackendExcel:
    def __init__(self, nombre_archivo="BaseDatosAlarma.xlsx"):
        self.__nombre_archivo = nombre_archivo
        self.preparar_archivo()

    def obtener_ruta_archivo(self):
        return self.__nombre_archivo

    def cambiar_ruta_archivo(self, nueva_ruta):
        self.__nombre_archivo = nueva_ruta
        self.preparar_archivo()

    # 1. CREACIÓN / PREPARACIÓN DEL ARCHIVO CON DOS HOJAS
    def preparar_archivo(self):
        try:
            libro = load_workbook(self.__nombre_archivo)
            # Verificar que existan ambas hojas
            if "Usuarios" not in libro.sheetnames:
                hoja_u = libro.create_sheet("Usuarios")
                hoja_u.append(["Fecha Registro", "Nombre Completo", "Tipo Documento", "Numero Documento"])
            if "Eventos_Alarma" not in libro.sheetnames:
                hoja_e = libro.create_sheet("Eventos_Alarma")
                hoja_e.append(["Fecha y Hora", "Operador", "Estado Sistema", "Evento / Accion"])
            libro.save(self.__nombre_archivo)
            libro.close()
        except FileNotFoundError:
            libro = Workbook()
            # Hoja 1: Datos personales
            hoja_usuarios = libro.active
            hoja_usuarios.title = "Usuarios"
            hoja_usuarios.append(["Fecha Registro", "Nombre Completo", "Tipo Documento", "Numero Documento"])

            # Hoja 2: Monitoreo e historial de la alarma
            hoja_eventos = libro.create_sheet("Eventos_Alarma")
            hoja_eventos.append(["Fecha y Hora", "Operador", "Estado Sistema", "Evento / Accion"])

            libro.save(self.__nombre_archivo)
            libro.close()

    # 2. ESCRITURA DE DATOS (Usuarios y Eventos)
    def registrar_usuario(self, usuario_obj):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Usuarios"]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hoja.append([
            fecha_actual,
            usuario_obj.consultar_nombre(),
            usuario_obj.consultar_tipo_documento(),
            usuario_obj.consultar_numero_documento()
        ])
        libro.save(self.__nombre_archivo)
        libro.close()

    def registrar_evento(self, operador, estado, descripcion):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Eventos_Alarma"]
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hoja.append([fecha_actual, operador, estado, descripcion])
        libro.save(self.__nombre_archivo)
        libro.close()

    # 3. LECTURA DE DATOS (Para alimentar los Treeview de monitoreo)
    def leer_usuarios(self):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Usuarios"]
        registros = []
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila[0] is not None:
                registros.append(fila)
        libro.close()
        return registros

    def leer_eventos(self):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Eventos_Alarma"]
        registros = []
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila[0] is not None:
                registros.append(fila)
        libro.close()
        return registros

    # 4. ACTUALIZACIÓN DE DATOS (Editar nombre o tipo de documento de un usuario)
    def actualizar_usuario(self, indice_fila, nuevo_nombre, nuevo_tipo, nuevo_doc):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Usuarios"]
        # indice_fila empieza en 0 desde el Treeview, en Excel la fila 1 es encabezado
        fila_excel = indice_fila + 2
        hoja.cell(row=fila_excel, column=2, value=nuevo_nombre)
        hoja.cell(row=fila_excel, column=3, value=nuevo_tipo)
        hoja.cell(row=fila_excel, column=4, value=nuevo_doc)
        libro.save(self.__nombre_archivo)
        libro.close()

    # 5. ELIMINACIÓN DE REGISTROS (En ambas hojas según selección)
    def eliminar_usuario(self, indice_fila):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Usuarios"]
        hoja.delete_rows(indice_fila + 2)
        libro.save(self.__nombre_archivo)
        libro.close()

    def eliminar_evento(self, indice_fila):
        libro = load_workbook(self.__nombre_archivo)
        hoja = libro["Eventos_Alarma"]
        hoja.delete_rows(indice_fila + 2)
        libro.save(self.__nombre_archivo)
        libro.close()

    # EXPORTAR COPIA (Para el menú "Guardar como")
    def guardar_copia_como(self, ruta_destino):
        libro = load_workbook(self.__nombre_archivo)
        libro.save(ruta_destino)
        libro.close()