"""DAO para Cita"""
import oracledb
from typing import List, Optional
from datetime import datetime
from models.cita import Cita
from database import get_connection

class CitaDAO:
    @staticmethod
    def create(cita: Cita) -> bool:
        sql = "INSERT INTO cita (id_cita, id_mascota, id_veterinario, fecha, hora, motivo, estado, diagnostico) VALUES (:id, :id_mascota, :id_vet, :fecha, :hora, :motivo, :estado, :diagnostico)"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": cita.id_cita, "id_mascota": cita.id_mascota, "id_vet": cita.id_veterinario, "fecha": cita.fecha, "hora": cita.hora, "motivo": cita.motivo, "estado": cita.estado, "diagnostico": cita.diagnostico})
                    conn.commit()
                    print(f"✓ Cita creada exitosamente.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: La mascota o veterinario no existen.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_cita: int) -> Optional[Cita]:
        sql = "SELECT * FROM cita WHERE id_cita = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_cita})
                    row = cursor.fetchone()
                    if not row:
                        print(f"✗ No se encontró cita con ID {id_cita}")
                        return None
                    id_c, id_m, id_v, fecha, hora, motivo, estado, diag = row
                    return Cita(id_c, id_m, id_v, fecha, hora, motivo, estado, diag)
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Cita]:
        sql = f"SELECT * FROM cita FETCH FIRST {limit} ROWS ONLY"
        citas = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    for row in cursor:
                        id_c, id_m, id_v, fecha, hora, motivo, estado, diag = row
                        citas.append(Cita(id_c, id_m, id_v, fecha, hora, motivo, estado, diag))
                    print(f"✓ Se encontraron {len(citas)} cita(s).")
                    return citas
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_mascota(id_mascota: int) -> List[Cita]:
        sql = "SELECT * FROM cita WHERE id_mascota = :id ORDER BY fecha DESC"
        citas = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_mascota})
                    for row in cursor:
                        id_c, id_m, id_v, fecha, hora, motivo, estado, diag = row
                        citas.append(Cita(id_c, id_m, id_v, fecha, hora, motivo, estado, diag))
                    return citas
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def read_by_veterinario(id_vet: int) -> List[Cita]:
        sql = "SELECT * FROM cita WHERE id_veterinario = :id ORDER BY fecha DESC"
        citas = []
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_vet})
                    for row in cursor:
                        id_c, id_m, id_v, fecha, hora, motivo, estado, diag = row
                        citas.append(Cita(id_c, id_m, id_v, fecha, hora, motivo, estado, diag))
                    return citas
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def update(cita: Cita) -> bool:
        sql = "UPDATE cita SET id_mascota=:id_mascota, id_veterinario=:id_vet, fecha=:fecha, hora=:hora, motivo=:motivo, estado=:estado, diagnostico=:diagnostico WHERE id_cita=:id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_mascota": cita.id_mascota, "id_vet": cita.id_veterinario, "fecha": cita.fecha, "hora": cita.hora, "motivo": cita.motivo, "estado": cita.estado, "diagnostico": cita.diagnostico, "id": cita.id_cita})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró cita con ID {cita.id_cita}")
                        return False
                    conn.commit()
                    print(f"✓ Cita ID {cita.id_cita} actualizada.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def delete(id_cita: int) -> bool:
        sql = "DELETE FROM cita WHERE id_cita = :id"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id": id_cita})
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró cita con ID {id_cita}")
                        return False
                    conn.commit()
                    print(f"✓ Cita ID {id_cita} eliminada.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            raise
    
    @staticmethod
    def create_with_sequence() -> int:
        sql = "SELECT seq_cita.NEXTVAL FROM DUAL"
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error: {e}")
            return -1
