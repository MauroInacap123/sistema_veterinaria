"""Módulo: models/veterinario.py - Clase Veterinario"""
from typing import Optional

class Veterinario:
    """Clase que representa un veterinario"""
    
    def __init__(self, id_veterinario: int, nombre: str, apellido: str, especialidad: str, telefono: str, email: str):
        self._id_veterinario = id_veterinario
        self._nombre = nombre
        self._apellido = apellido
        self._especialidad = especialidad
        self._telefono = telefono
        self._email = email
    
    @property
    def id_veterinario(self) -> int:
        return self._id_veterinario
    
    @id_veterinario.setter
    def id_veterinario(self, value: int):
        if value <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        self._id_veterinario = value
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value.strip()
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @apellido.setter
    def apellido(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("El apellido no puede estar vacío")
        self._apellido = value.strip()
    
    @property
    def especialidad(self) -> str:
        return self._especialidad
    
    @especialidad.setter
    def especialidad(self, value: str):
        self._especialidad = value.strip() if value else ""
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    @telefono.setter
    def telefono(self, value: str):
        self._telefono = value.strip() if value else ""
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if value and "@" not in value:
            raise ValueError("El email debe tener formato válido")
        self._email = value.strip() if value else ""
    
    def obtener_nombre_completo(self) -> str:
        return f"{self._nombre} {self._apellido}"
    
    def __str__(self) -> str:
        return f"Veterinario(ID: {self._id_veterinario}, Nombre: {self.obtener_nombre_completo()}, Especialidad: {self._especialidad})"
    
    def to_dict(self) -> dict:
        return {
            "id_veterinario": self._id_veterinario, "nombre": self._nombre, "apellido": self._apellido,
            "especialidad": self._especialidad, "telefono": self._telefono, "email": self._email,
            "nombre_completo": self.obtener_nombre_completo()
        }
