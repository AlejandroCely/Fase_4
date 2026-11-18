# John Alejandro Cely Roa
# Curso Programacion 213023
# Fase 4 - Sistema de clientes y servicios

# Se importan las herramientas que se utilizan en el programa.
from abc import ABC, abstractmethod
import logging
from pathlib import Path
import re


# El archivo de eventos y errores se guarda junto a este programa.
logging.basicConfig(filename=str(Path(__file__).with_name("software_fj.log")),level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8")


# Estas excepciones permiten reconocer errores de datos.
class ErrorSistema(Exception):
    pass


class DatoInvalidoError(ErrorSistema):
    pass


# Entidad es una clase general para los elementos del sistema.
class Entidad(ABC):

    def __init__(self, codigo):
        codigo = str(codigo).strip()
        if codigo == "":
            raise DatoInvalidoError("El codigo no puede estar vacio.")
        self._codigo = codigo

    @property
    def codigo(self):
        return self._codigo

# Cada clase que hereda de Entidad define cómo mostrar sus datos.
    @abstractmethod
    def mostrar_datos(self):
        pass


# Cliente guarda y valida el nombre, el documento y el correo.
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
        return (self.codigo + " - " + self.get_nombre() + " - " + self.get_documento() + " - " + self.get_correo())


# Servicio es una clase general. Cada servicio calcula su propio costo.
class Servicio(Entidad):

    def __init__(self, codigo, nombre, tarifa):
        super().__init__(codigo)
        nombre = str(nombre).strip()
        tarifa = float(tarifa)
        if nombre == "" or tarifa <= 0:
            raise DatoInvalidoError("El servicio debe tener nombre y tarifa mayor que cero.")
        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def validar(self, duracion, datos):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, cantidad=1):
        pass

    def calcular_total(self, duracion, impuesto=0, descuento=0, cantidad=1):

    # Los valores opcionales permiten calcular con impuesto y descuento.
        impuesto = float(impuesto)
        descuento = float(descuento)
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatoInvalidoError("Impuesto y descuento deben estar entre 0 y 100.")

        costo = self.calcular_costo(duracion, cantidad)
        costo = costo * (1 - descuento / 100)
        return costo * (1 + impuesto / 100)


# La sala se cobra por hora y tiene un limite de personas.
class Sala(Servicio):

    def __init__(self, codigo, nombre, tarifa_hora, capacidad):
        super().__init__(codigo, nombre, tarifa_hora)
        self.capacidad = int(capacidad)
        if self.capacidad <= 0:
            raise DatoInvalidoError("La capacidad debe ser mayor que cero.")

    def validar(self, duracion, datos):
        try:
            personas = int(datos.get("personas", 0))
        except (TypeError, ValueError) as error:
            raise DatoInvalidoError("La cantidad de personas debe ser un numero.") from error

        if duracion <= 0 or duracion > 12:
            raise DatoInvalidoError("La sala se puede reservar de 1 a 12 horas.")
        if personas <= 0 or personas > self.capacidad:
            raise DatoInvalidoError("La cantidad de personas no es valida para esta sala.")

    def calcular_costo(self, duracion, cantidad=1):
        return self.tarifa * float(duracion)

    def mostrar_datos(self):
        return self.codigo + " - Sala: " + self.nombre + " | Capacidad: " + str(self.capacidad)


# El equipo se cobra por dia y por cada unidad solicitada.
class Equipo(Servicio):

    def __init__(self, codigo, nombre, tarifa_dia, disponibles):
        super().__init__(codigo, nombre, tarifa_dia)
        self.disponibles = int(disponibles)
        if self.disponibles < 0:
            raise DatoInvalidoError("Las unidades disponibles no pueden ser negativas.")

    def validar(self, duracion, datos):
        try:
            cantidad = int(datos.get("cantidad", 0))
        except (TypeError, ValueError) as error:
            raise DatoInvalidoError("La cantidad de equipos debe ser un numero.") from error

        if duracion <= 0 or duracion > 30:
            raise DatoInvalidoError("El alquiler se puede hacer de 1 a 30 dias.")
        if cantidad <= 0 or cantidad > self.disponibles:
            raise DatoInvalidoError("No hay suficientes equipos disponibles.")

    def calcular_costo(self, duracion, cantidad=1):
        return self.tarifa * float(duracion) * int(cantidad)

    def mostrar_datos(self):
        return self.codigo + " - Equipo: " + self.nombre + " | Disponibles: " + str(self.disponibles)


# La asesoria se cobra por hora y necesita un tema.
class Asesoria(Servicio):

    def validar(self, duracion, datos):
        tema = str(datos.get("tema", "")).strip()
        if duracion <= 0 or duracion > 8:
            raise DatoInvalidoError("La asesoria se puede reservar de 1 a 8 horas.")
        if tema == "":
            raise DatoInvalidoError("Debe escribir el tema de la asesoria.")

    def calcular_costo(self, duracion, cantidad=1):
        return self.tarifa * float(duracion)

    def mostrar_datos(self):
        return self.codigo + " - Asesoria: " + self.nombre


# Esta funcion muestra como responden el cliente y los servicios ante diferentes datos.
def probar_cliente_y_servicios():

# Se intenta crear un cliente con datos que cumplen las validaciones.
    print("Prueba de cliente valido:")
    try:
        cliente = Cliente("C01", "Ana Torres", "90778332", "ana@email.com")

# Se registra el evento y se muestran los datos del cliente creado.
        logging.info("Cliente creado: %s", cliente.codigo)
        print(cliente.mostrar_datos())
    except ErrorSistema as error:

# Si un dato no es correcto, se guarda el error y se informa sin cerrar el programa.
        logging.exception("No se pudo crear el cliente.")
        print("Error controlado: " + str(error))

# En esta prueba el correo tiene un formato incorrecto. La idea es comprobar que la validacion detecta el dato y permite continuar.
    print("\nPrueba de correo incorrecto:")
    try:
        Cliente("C02", "Luis Perez", "12345678", "correo-malo")
    except ErrorSistema as error:
        logging.exception("Se detecto un dato de cliente incorrecto.")
        print("Error controlado: " + str(error))

# Se crean un ejemplo de cada servicio con sus tarifas y caracteristicas.
    print("\nPrueba de servicios:")
    sala = Sala("S01", "Sala Norte", 50000, 20)
    equipo = Equipo("S02", "Proyector", 80000, 3)
    asesoria = Asesoria("S03", "Asesoria de software", 60000)

# Se muestra la informacion de la sala y se prueba su costo de dos horas.
    print(sala.mostrar_datos())
    print("Costo de sala por 2 horas: $" + format(sala.calcular_costo(2), ",.0f"))

# El segundo ejemplo agrega el impuesto y el tercero agrega impuesto y descuento.
    print("Costo de sala con impuesto: $" + format(sala.calcular_total(2, 19), ",.0f"))
    print("Costo de sala con impuesto y descuento: $" + format(sala.calcular_total(2, 19, 10), ",.0f"))

# El costo del equipo depende de los dias y de la cantidad solicitada.
    print(equipo.mostrar_datos())
    print("Costo de 2 equipos por 2 dias: $" + format(equipo.calcular_costo(2, 2), ",.0f"))

# La asesoria se cobra por hora.
    print(asesoria.mostrar_datos())
    print("Costo de asesoria por 1 hora: $" + format(asesoria.calcular_costo(1), ",.0f"))

 # Se intenta crear una sala con tarifa negativa para comprobar la validacion.
    print("\nPrueba de servicio con tarifa incorrecta:")
    try:
        Sala("S04", "Sala invalida", -1000, 10)
    except ErrorSistema as error:
        logging.exception("La tarifa de la sala no es valida.")
        print("Error controlado: " + str(error))

# La sala solo permite el numero de personas indicado en su capacidad.
    print("\nPrueba de sala con demasiadas personas:")
    try:
        sala.validar(2, {"personas": 25})
    except ErrorSistema as error:
        logging.exception("La cantidad de personas supera la capacidad.")
        print("Error controlado: " + str(error))

# Se solicita una cantidad de equipos mayor a la que hay disponible.
    print("\nPrueba de equipo no disponible:")
    try:
        equipo.validar(2, {"cantidad": 4})
    except ErrorSistema as error:
        logging.exception("No hay suficientes equipos para la prueba.")
        print("Error controlado: " + str(error))

# La asesoria necesita un tema; esta prueba deja el dato vacio a proposito.
    print("\nPrueba de asesoria sin tema:")
    try:
        asesoria.validar(1, {"tema": ""})
    except ErrorSistema as error:
        logging.exception("La prueba de asesoria no tiene tema.")
        print("Error controlado: " + str(error))


# Esta parte ejecuta las comprobaciones cuando se abre el archivo.
if __name__ == "__main__":
    probar_cliente_y_servicios()
