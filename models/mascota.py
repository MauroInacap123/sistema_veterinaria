"""Módulo: models/mascota.py - Clase Mascota"""
from typing import Optional

class Mascota:
    """Clase que representa una mascota"""
    
    ESPECIE_PERRO = "PERRO"
    ESPECIE_GATO = "GATO"
    ESPECIE_AVE = "AVE"
    ESPECIE_CONEJO = "CONEJO"
    ESPECIE_HAMSTER = "HAMSTER"
    ESPECIES_VALIDAS = [ESPECIE_PERRO, ESPECIE_GATO, ESPECIE_AVE, ESPECIE_CONEJO, ESPECIE_HAMSTER]
    
    def __init__(self, id_mascota: int, nombre: str, especie: str, raza: str, edad: int, color: str, peso: float, id_cliente: int):
        self._id_mascota = id_mascota
        self._nombre = nombre
        self._especie = especie
        self._raza = raza
        self._edad = edad
        self._color = color
        self._peso = peso
        self._id_cliente = id_cliente
    
    @property
    def id_mascota(self) -> int:
        return self._id_mascota
    
    @id_mascota.setter
    def id_mascota(self, value: int):
        if value <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        self._id_mascota = value
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip()
    
    @property
    def especie(self) -> str:
        return self._especie
    
    @especie.setter
    def especie(self, value: str):
        value_upper = value.upper()
        if value_upper not in self.ESPECIES_VALIDAS:
            raise ValueError(f"Especie inválida. Debe ser: {', '.join(self.ESPECIES_VALIDAS)}")
        self._especie = value_upper
    
    @property
    def raza(self) -> str:
        return self._raza
    
    @raza.setter
    def raza(self, value: str):
        self._raza = value.strip() if value else ""
    
    @property
    def edad(self) -> int:
        return self._edad
    
    @edad.setter
    def edad(self, value: int):
        if value < 0:
            raise ValueError("La edad no puede ser negativa")
        if value > 50:
            raise ValueError("La edad parece incorrecta (máx 50 años)")
        self._edad = value
    
    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, value: str):
        self._color = value.strip() if value else ""
    
    @property
    def peso(self) -> float:
        return self._peso
    
    @peso.setter
    def peso(self, value: float):
        if value <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        if value > 500:
            raise ValueError("El peso parece incorrecto")
        self._peso = value
    
    @property
    def id_cliente(self) -> int:
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente(self, value: int):
        if value <= 0:
            raise ValueError("El ID del cliente debe ser mayor a 0")
        self._id_cliente = value
    
    def es_cachorro(self) -> bool:
        """Determina si es cachorro (< 1 año)"""
        return self._edad < 1
    
    def es_senior(self) -> bool:
        """Determina si es senior (> 7 años)"""
        if self._especie in [self.ESPECIE_PERRO, self.ESPECIE_GATO]:
            return self._edad > 7
        return False
    
    def __str__(self) -> str:
        return f"Mascota(ID: {self._id_mascota}, Nombre: {self._nombre}, Especie: {self._especie}, Raza: {self._raza}, Edad: {self._edad} años, Peso: {self._peso} kg)"
    
    def __repr__(self) -> str:
        return f"Mascota({self._id_mascota}, '{self._nombre}', '{self._especie}')"
    
    def to_dict(self) -> dict:
        return {
            "id_mascota": self._id_mascota, "nombre": self._nombre, "especie": self._especie, "raza": self._raza,
            "edad": self._edad, "color": self._color, "peso": self._peso, "id_cliente": self._id_cliente,
            "es_cachorro": self.es_cachorro(), "es_senior": self.es_senior()
        }
