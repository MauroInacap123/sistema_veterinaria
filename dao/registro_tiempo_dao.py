"""
Módulo: dao/registro_tiempo_dao.py
Data Access Object para la entidad RegistroTiempo
"""

import oracledb
from typing import List, Optional
from models.registro_tiempo import RegistroTiempo
from database import get_connection


class RegistroTiempoDAO:
    """Clase para manejar operaciones CRUD de RegistroTiempo"""
    
    @staticmethod
    def create(registro: RegistroTiempo) -> bool:
        """Crea un nuevo registro de tiempo en la base de datos"""
        sql = """
            INSERT INTO registro_tiempo 
            (id_registro, id_empleado, id_proyecto, fecha, horas_trabajadas, descripcion_actividad)
            VALUES 
            (:id_registro, :id_empleado, :id_proyecto, :fecha, :horas_trabajadas, :descripcion_actividad)
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "id_registro": registro.id_registro,
                        "id_empleado": registro.id_empleado,
                        "id_proyecto": registro.id_proyecto,
                        "fecha": registro.fecha,
                        "horas_trabajadas": registro.horas_trabajadas,
                        "descripcion_actividad": registro.descripcion_actividad
                    })
                    conn.commit()
                    print(f"✓ Registro de tiempo creado exitosamente.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: Problema de integridad al crear registro.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error de base de datos: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_registro: int) -> Optional[RegistroTiempo]:
        """Lee un registro de tiempo por su ID"""
        sql = "SELECT * FROM registro_tiempo WHERE id_registro = :id_registro"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_registro": id_registro})
                    row = cursor.fetchone()
                    
                    if not row:
                        print(f"✗ No se encontró registro con ID {id_registro}")
                        return None
                    
                    return RegistroTiempoDAO._row_to_registro(row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer registro: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[RegistroTiempo]:
        """Lee todos los registros de tiempo"""
        sql = f"SELECT * FROM registro_tiempo FETCH FIRST {limit} ROWS ONLY"
        registros = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    
                    for row in cursor:
                        registros.append(RegistroTiempoDAO._row_to_registro(row))
                    
                    print(f"✓ Se encontraron {len(registros)} registro(s).")
                    return registros
        except oracledb.DatabaseError as e:
            print(f"✗ Error al listar registros: {e}")
            raise
    
    @staticmethod
    def read_by_empleado(id_empleado: int) -> List[RegistroTiempo]:
        """Lee todos los registros de un empleado"""
        sql = "SELECT * FROM registro_tiempo WHERE id_empleado = :id_empleado"
        registros = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_empleado": id_empleado})
                    
                    for row in cursor:
                        registros.append(RegistroTiempoDAO._row_to_registro(row))
                    
                    return registros
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer registros por empleado: {e}")
            raise
    
    @staticmethod
    def read_by_proyecto(id_proyecto: int) -> List[RegistroTiempo]:
        """Lee todos los registros de un proyecto"""
        sql = "SELECT * FROM registro_tiempo WHERE id_proyecto = :id_proyecto"
        registros = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_proyecto": id_proyecto})
                    
                    for row in cursor:
                        registros.append(RegistroTiempoDAO._row_to_registro(row))
                    
                    return registros
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer registros por proyecto: {e}")
            raise
    
    @staticmethod
    def update(registro: RegistroTiempo) -> bool:
        """Actualiza un registro de tiempo existente"""
        sql = """
            UPDATE registro_tiempo 
            SET id_empleado = :id_empleado,
                id_proyecto = :id_proyecto,
                fecha = :fecha,
                horas_trabajadas = :horas_trabajadas,
                descripcion_actividad = :descripcion_actividad
            WHERE id_registro = :id_registro
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "id_empleado": registro.id_empleado,
                        "id_proyecto": registro.id_proyecto,
                        "fecha": registro.fecha,
                        "horas_trabajadas": registro.horas_trabajadas,
                        "descripcion_actividad": registro.descripcion_actividad,
                        "id_registro": registro.id_registro
                    })
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró registro con ID {registro.id_registro}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Registro ID {registro.id_registro} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error al actualizar registro: {e}")
            raise
    
    @staticmethod
    def delete(id_registro: int) -> bool:
        """Elimina un registro de tiempo por su ID"""
        sql = "DELETE FROM registro_tiempo WHERE id_registro = :id_registro"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_registro": id_registro})
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró registro con ID {id_registro}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Registro ID {id_registro} eliminado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error al eliminar registro: {e}")
            raise
    
    @staticmethod
    def _row_to_registro(row) -> RegistroTiempo:
        """Convierte una fila de la BD a objeto RegistroTiempo"""
        (id_reg, id_emp, id_proy, fecha, horas, descripcion) = row
        
        return RegistroTiempo(
            id_registro=id_reg,
            id_empleado=id_emp,
            id_proyecto=id_proy,
            fecha=fecha,
            horas_trabajadas=float(horas),
            descripcion_actividad=descripcion if descripcion else ""
        )
    
    @staticmethod
    def create_with_sequence() -> int:
        """Obtiene el siguiente ID de la secuencia"""
        sql = "SELECT seq_registro.NEXTVAL FROM DUAL"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error al obtener siguiente ID: {e}")
            return -1
