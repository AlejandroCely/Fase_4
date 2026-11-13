# John Alejandro Cely Roa
# Curso Programacion 213023
# Fase 4 - Etapa 1: estructura inicial y clase Cliente

# Se importan las herramientas para clases abstractas, registros y validacion del correo.
from abc import ABC, abstractmethod
import logging
from pathlib import Path
import re


# El archivo de eventos y errores se guarda junto a este programa.
logging.basicConfig(
    filename=str(Path(__file__).with_name("software_fj.log")),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# Estas excepciones permiten reconocer errores de datos.
class ErrorSistema(Exception):
    pass


class DatoInvalidoError(ErrorSistema):
    pass


# Cada clase que hereda de Entidad define cómo mostrar sus propios datos.
class Entidad(ABC):

    def __init__(self, codigo):
        codigo = str(codigo).strip()
        if codigo == "":
            raise DatoInvalidoError("El codigo no puede estar vacio.")
        self._codigo = codigo

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def mostrar_datos(self):
        pass


# Cliente hereda de Entidad y revisa sus datos antes de guardarlos.
class Cliente(Entidad):

    def __init__(self, codigo, nombre, documento, correo):
        super().__init__(codigo)
        self.set_nombre(nombre)
        self.set_documento(documento)
        self.set_correo(correo)

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        if not self.validar_nombre(nombre):
            raise DatoInvalidoError("El nombre debe tener al menos dos letras.")
        self._nombre = str(nombre).strip()

    def get_documento(self):
        return self._documento

    def set_documento(self, documento):
        if not self.validar_documento(documento):
            raise DatoInvalidoError("El documento debe tener entre 6 y 15 digitos.")
        self._documento = str(documento).strip()

    def get_correo(self):
        return self._correo

    def set_correo(self, correo):
        if not self.validar_correo(correo):
            raise DatoInvalidoError("El correo no tiene un formato valido.")
        self._correo = str(correo).strip()

    def validar_nombre(self, nombre):
        nombre = str(nombre).strip()
        return len(nombre) >= 2 and all(letra.isalpha() or letra.isspace() for letra in nombre)

    def validar_documento(self, documento):
        documento = str(documento).strip()
        return documento.isdigit() and 6 <= len(documento) <= 15

    def validar_correo(self, correo):
        correo = str(correo).strip()
        return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo) is not None

    def mostrar_datos(self):
        return (self.codigo + " - " + self.get_nombre() + " - " + self.get_documento()
                + " - " + self.get_correo())


# Esta prueba muestra un cliente correcto y uno con datos incorrectos.
def probar_clientes():
    print("Prueba de cliente valido:")
    try:
        cliente = Cliente("C01", "Ana Torres", "1022325325", "ana@email.com")
        logging.info("Cliente de prueba creado: %s", cliente.codigo)
        print(cliente.mostrar_datos())
    except ErrorSistema as error:
        logging.exception("No se pudo crear el cliente de prueba.")
        print("Error controlado: " + str(error))

    print("\nPrueba de cliente con correo incorrecto:")
    try:
        Cliente("C02", "Luis Perez", "12345678", "correo-malo")
    except ErrorSistema as error:
        logging.exception("Se detecto un dato de cliente incorrecto.")
        print("Error controlado: " + str(error))


# Esta parte ejecuta las pruebas cuando se abre el archivo.
if __name__ == "__main__":
    probar_clientes()
