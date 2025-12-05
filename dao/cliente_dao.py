"""DAO para Cliente"""
import oracledb
from typing import List, Optional
from models.cliente import Cliente
from database import get_connection

class ClienteDAO:
    @staticmethod
    def create(cliente: Cliente) -> bool:
        sql = "INSERT INTO cliente (id_cliente, rut, nombres, apellidos, telefono, email, direccion) VALUES (:id, :rut, :nombres, :apellidos, :telefono, :email, :direccion)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": cliente.id_cliente, "rut": cliente.rut, "nombres": cliente.nombres, "apellidos": cliente.apellidos, "telefono": cliente.telefono, "email": cliente.email, "direccion": cliente.direccion})
                    conn.commit()
                    print(f"✓ Cliente '{cliente.obtener_nombre_completo()}' creado exitosamente.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: El cliente ya existe.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error de base de datos: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_cliente: int) -> Optional[Cliente]:
        sql = "SELECT * FROM cliente WHERE id_cliente = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_cliente})
                    row = cursor.fetchone()
                    if not row:
                        print(f"✗ No se encontró cliente con ID {id_cliente}")
                        return None
                    return Cliente(*row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Cliente]:
        sql = f"SELECT * FROM cliente FETCH FIRST {limit} ROWS ONLY"
        clientes = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    for row in cursor:
                        clientes.append(Cliente(*row))
                    print(f"✓ Se encontraron {len(clientes)} cliente(s).")
                    return clientes
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def update(cliente: Cliente) -> bool:
        sql = "UPDATE cliente SET rut=:rut, nombres=:nombres, apellidos=:apellidos, telefono=:telefono, email=:email, direccion=:direccion WHERE id_cliente=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"rut": cliente.rut, "nombres": cliente.nombres, "apellidos": cliente.apellidos, "telefono": cliente.telefono, "email": cliente.email, "direccion": cliente.direccion, "id": cliente.id_cliente})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró cliente con ID {cliente.id_cliente}")
                        return False
                    conn.commit()
                    print(f"✓ Cliente ID {cliente.id_cliente} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def delete(id_cliente: int) -> bool:
        sql = "DELETE FROM cliente WHERE id_cliente = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_cliente})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró cliente con ID {id_cliente}")
                        return False
                    conn.commit()
                    print(f"✓ Cliente ID {id_cliente} eliminado.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: No se puede eliminar el cliente porque tiene mascotas asignadas.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def create_with_sequence() -> int:
        sql = "SELECT seq_cliente.NEXTVAL FROM DUAL"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            return -1
