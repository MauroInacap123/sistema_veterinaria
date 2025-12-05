"""Módulo: models/cita.py - Clase Cita"""
from datetime import date, datetime
from typing import Optional

class Cita:
    """Clase que representa una cita veterinaria"""
    
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_COMPLETADA = "COMPLETADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADOS_VALIDOS = [ESTADO_PENDIENTE, ESTADO_CONFIRMADA, ESTADO_COMPLETADA, ESTADO_CANCELADA]
    
    def __init__(self, id_cita: int, id_mascota: int, id_veterinario: int, fecha: date, hora: str, motivo: str, estado: str = ESTADO_PENDIENTE, diagnostico: Optional[str] = None):
        self._id_cita = id_cita
        self._id_mascota = id_mascota
        self._id_veterinario = id_veterinario
        self._fecha = fecha
        self._hora = hora
        self._motivo = motivo
        self._estado = estado
        self._diagnostico = diagnostico
    
    @property
    def id_cita(self) -> int:
        return self._id_cita
    
    @id_cita.setter
    def id_cita(self, value: int):
        if value <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        self._id_cita = value
    
    @property
    def id_mascota(self) -> int:
        return self._id_mascota
    
    @id_mascota.setter
    def id_mascota(self, value: int):
        if value <= 0:
            raise ValueError("El ID de la mascota debe ser mayor a 0")
        self._id_mascota = value
    
    @property
    def id_veterinario(self) -> int:
        return self._id_veterinario
    
    @id_veterinario.setter
    def id_veterinario(self, value: int):
        if value <= 0:
            raise ValueError("El ID del veterinario debe ser mayor a 0")
        self._id_veterinario = value
    
    @property
    def fecha(self) -> date:
        return self._fecha
    
    @fecha.setter
    def fecha(self, value: date):
        self._fecha = value
    
    @property
    def hora(self) -> str:
        return self._hora
    
    @hora.setter
    def hora(self, value: str):
        self._hora = value.strip()
    
    @property
    def motivo(self) -> str:
        return self._motivo
    
    @motivo.setter
    def motivo(self, value: str):
        self._motivo = value.strip() if value else ""
    
    @property
    def estado(self) -> str:
        return self._estado
    
    @estado.setter
    def estado(self, value: str):
        if value not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Debe ser: {', '.join(self.ESTADOS_VALIDOS)}")
        self._estado = value
    
    @property
    def diagnostico(self) -> Optional[str]:
        return self._diagnostico
    
    @diagnostico.setter
    def diagnostico(self, value: Optional[str]):
        self._diagnostico = value.strip() if value else None
    
    def esta_pendiente(self) -> bool:
        return self._estado == self.ESTADO_PENDIENTE
    
    def esta_completada(self) -> bool:
        return self._estado == self.ESTADO_COMPLETADA
    
    def __str__(self) -> str:
        return f"Cita(ID: {self._id_cita}, Mascota ID: {self._id_mascota}, Veterinario ID: {self._id_veterinario}, Fecha: {self._fecha}, Hora: {self._hora}, Estado: {self._estado})"
    
    def to_dict(self) -> dict:
        return {
            "id_cita": self._id_cita, "id_mascota": self._id_mascota, "id_veterinario": self._id_veterinario,
            "fecha": self._fecha.isoformat() if self._fecha else None, "hora": self._hora, "motivo": self._motivo,
            "estado": self._estado, "diagnostico": self._diagnostico,
            "esta_pendiente": self.esta_pendiente(), "esta_completada": self.esta_completada()
        }
