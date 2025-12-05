"""
Módulo: models/cliente.py
Clase que representa un Cliente (dueño de mascotas)
"""

from typing import Optional


class Cliente:
    """Clase que representa un cliente de la veterinaria"""
    
    def __init__(
        self,
        id_cliente: int,
        rut: str,
        nombres: str,
        apellidos: str,
        telefono: str,
        email: str,
        direccion: Optional[str] = None
    ):
        self._id_cliente = id_cliente
        self._rut = rut
        self._nombres = nombres
        self._apellidos = apellidos
        self._telefono = telefono
        self._email = email
        self._direccion = direccion
    
    @property
    def id_cliente(self) -> int:
        return self._id_cliente
    
    @id_cliente.setter
    def id_cliente(self, value: int):
        if value <= 0:
            raise ValueError("El ID debe ser mayor a 0")
        self._id_cliente = value
    
    @property
    def rut(self) -> str:
        return self._rut
    
    @rut.setter
    def rut(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("El RUT no puede estar vacío")
        self._rut = value.strip()
    
    @property
    def nombres(self) -> str:
        return self._nombres
    
    @nombres.setter
    def nombres(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Los nombres no pueden estar vacíos")
        self._nombres = value.strip()
    
    @property
    def apellidos(self) -> str:
        return self._apellidos
    
    @apellidos.setter
    def apellidos(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Los apellidos no pueden estar vacíos")
        self._apellidos = value.strip()
    
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
    
    @property
    def direccion(self) -> Optional[str]:
        return self._direccion
    
    @direccion.setter
    def direccion(self, value: Optional[str]):
        self._direccion = value.strip() if value else None
    
    def obtener_nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente"""
        return f"{self._nombres} {self._apellidos}"
    
    def __str__(self) -> str:
        return (f"Cliente(ID: {self._id_cliente}, "
                f"RUT: {self._rut}, "
                f"Nombre: {self.obtener_nombre_completo()}, "
                f"Email: {self._email})")
    
    def __repr__(self) -> str:
        return (f"Cliente({self._id_cliente}, '{self._rut}', "
                f"'{self._nombres}', '{self._apellidos}')")
    
    def to_dict(self) -> dict:
        return {
            "id_cliente": self._id_cliente,
            "rut": self._rut,
            "nombres": self._nombres,
            "apellidos": self._apellidos,
            "telefono": self._telefono,
            "email": self._email,
            "direccion": self._direccion,
            "nombre_completo": self.obtener_nombre_completo()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id_cliente=data.get("id_cliente"),
            rut=data.get("rut"),
            nombres=data.get("nombres"),
            apellidos=data.get("apellidos"),
            telefono=data.get("telefono", ""),
            email=data.get("email", ""),
            direccion=data.get("direccion")
        )
