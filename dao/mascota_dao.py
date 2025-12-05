"""DAO para Mascota"""
import oracledb
from typing import List, Optional
from models.mascota import Mascota
from database import get_connection

class MascotaDAO:
    @staticmethod
    def create(mascota: Mascota) -> bool:
        sql = "INSERT INTO mascota (id_mascota, nombre, especie, raza, edad, color, peso, id_cliente) VALUES (:id, :nombre, :especie, :raza, :edad, :color, :peso, :id_cliente)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": mascota.id_mascota, "nombre": mascota.nombre, "especie": mascota.especie, "raza": mascota.raza, "edad": mascota.edad, "color": mascota.color, "peso": mascota.peso, "id_cliente": mascota.id_cliente})
                    conn.commit()
                    print(f"✓ Mascota '{mascota.nombre}' creada exitosamente.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: La mascota ya existe o el cliente no existe.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_mascota: int) -> Optional[Mascota]:
        sql = "SELECT * FROM mascota WHERE id_mascota = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_mascota})
                    row = cursor.fetchone()
                    if not row:
                        print(f"✗ No se encontró mascota con ID {id_mascota}")
                        return None
                    return Mascota(*row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Mascota]:
        sql = f"SELECT * FROM mascota FETCH FIRST {limit} ROWS ONLY"
        mascotas = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    for row in cursor:
                        mascotas.append(Mascota(*row))
                    print(f"✓ Se encontraron {len(mascotas)} mascota(s).")
                    return mascotas
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_cliente(id_cliente: int) -> List[Mascota]:
        sql = "SELECT * FROM mascota WHERE id_cliente = :id"
        mascotas = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_cliente})
                    for row in cursor:
                        mascotas.append(Mascota(*row))
                    return mascotas
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def update(mascota: Mascota) -> bool:
        sql = "UPDATE mascota SET nombre=:nombre, especie=:especie, raza=:raza, edad=:edad, color=:color, peso=:peso, id_cliente=:id_cliente WHERE id_mascota=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"nombre": mascota.nombre, "especie": mascota.especie, "raza": mascota.raza, "edad": mascota.edad, "color": mascota.color, "peso": mascota.peso, "id_cliente": mascota.id_cliente, "id": mascota.id_mascota})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró mascota con ID {mascota.id_mascota}")
                        return False
                    conn.commit()
                    print(f"✓ Mascota ID {mascota.id_mascota} actualizada.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def delete(id_mascota: int) -> bool:
        sql = "DELETE FROM mascota WHERE id_mascota = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_mascota})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró mascota con ID {id_mascota}")
                        return False
                    conn.commit()
                    print(f"✓ Mascota ID {id_mascota} eliminada.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: No se puede eliminar la mascota porque tiene citas asociadas.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def create_with_sequence() -> int:
        sql = "SELECT seq_mascota.NEXTVAL FROM DUAL"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            return -1
