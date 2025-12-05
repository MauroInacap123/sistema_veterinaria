"""DAO para Veterinario"""
import oracledb
from typing import List, Optional
from models.veterinario import Veterinario
from database import get_connection

class VeterinarioDAO:
    @staticmethod
    def create(vet: Veterinario) -> bool:
        sql = "INSERT INTO veterinario (id_veterinario, nombre, apellido, especialidad, telefono, email) VALUES (:id, :nombre, :apellido, :especialidad, :telefono, :email)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": vet.id_veterinario, "nombre": vet.nombre, "apellido": vet.apellido, "especialidad": vet.especialidad, "telefono": vet.telefono, "email": vet.email})
                    conn.commit()
                    print(f"✓ Veterinario '{vet.obtener_nombre_completo()}' creado exitosamente.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: El veterinario ya existe.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_vet: int) -> Optional[Veterinario]:
        sql = "SELECT * FROM veterinario WHERE id_veterinario = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_vet})
                    row = cursor.fetchone()
                    if not row:
                        print(f"✗ No se encontró veterinario con ID {id_vet}")
                        return None
                    return Veterinario(*row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Veterinario]:
        sql = f"SELECT * FROM veterinario FETCH FIRST {limit} ROWS ONLY"
        vets = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    for row in cursor:
                        vets.append(Veterinario(*row))
                    print(f"✓ Se encontraron {len(vets)} veterinario(s).")
                    return vets
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def update(vet: Veterinario) -> bool:
        sql = "UPDATE veterinario SET nombre=:nombre, apellido=:apellido, especialidad=:especialidad, telefono=:telefono, email=:email WHERE id_veterinario=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"nombre": vet.nombre, "apellido": vet.apellido, "especialidad": vet.especialidad, "telefono": vet.telefono, "email": vet.email, "id": vet.id_veterinario})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró veterinario con ID {vet.id_veterinario}")
                        return False
                    conn.commit()
                    print(f"✓ Veterinario ID {vet.id_veterinario} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def delete(id_vet: int) -> bool:
        sql = "DELETE FROM veterinario WHERE id_veterinario = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_vet})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró veterinario con ID {id_vet}")
                        return False
                    conn.commit()
                    print(f"✓ Veterinario ID {id_vet} eliminado.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: No se puede eliminar el veterinario porque tiene citas asignadas.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def create_with_sequence() -> int:
        sql = "SELECT seq_veterinario.NEXTVAL FROM DUAL"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            return -1
