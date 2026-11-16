# CLASE PARA MODELAR Y VALIDAR AL USUARIO OPERADOR
class UsuarioAutorizado:
    def __init__(self, nombre, tipo_documento, numero_documento):
        self.__nombre = ""
        self.__tipo_documento = ""
        self.__numero_documento = ""

        # Usamos los setters para aplicar validaciones desde la creación
        self.establecer_datos(nombre, tipo_documento, numero_documento)

    def establecer_datos(self, nombre, tipo_documento, numero_documento):
        nombre_limpio = nombre.strip()
        doc_limpio = numero_documento.strip()

        # Validación 1: El nombre no puede estar vacío ni tener números
        if not nombre_limpio or any(char.isdigit() for char in nombre_limpio):
            raise ValueError("El nombre no puede estar vacío ni contener números.")

        # Validación 2: El tipo de documento debe ser válido
        if tipo_documento not in ["Cédula de Ciudadanía", "Tarjeta de Identidad"]:
            raise ValueError("Seleccione un tipo de documento válido.")

        # Validación 3: El documento debe ser numérico y tener longitud coherente
        if not doc_limpio.isdigit() or len(doc_limpio) < 6 or len(doc_limpio) > 12:
            raise ValueError("El número de documento debe tener entre 6 y 12 dígitos numéricos.")

        self.__nombre = nombre_limpio.title()
        self.__tipo_documento = tipo_documento
        self.__numero_documento = doc_limpio

    # Métodos de consulta (Getters)
    def consultar_nombre(self):
        return self.__nombre

    def consultar_tipo_documento(self):
        return self.__tipo_documento

    def consultar_numero_documento(self):
        return self.__numero_documento

    def obtener_diccionario(self):
        return {
            "nombre": self.__nombre,
            "tipo_documento": self.__tipo_documento,
            "numero_documento": self.__numero_documento
        }