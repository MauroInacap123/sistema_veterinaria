"""
Módulo: dao/proyecto_dao.py
Data Access Object para la entidad Proyecto
"""

import oracledb
from typing import List, Optional
from models.proyecto import Proyecto
from database import get_connection


class ProyectoDAO:
    """Clase para manejar operaciones CRUD de Proyecto"""
    
    @staticmethod
    def create(proyecto: Proyecto) -> bool:
        """Crea un nuevo proyecto en la base de datos"""
        sql = """
            INSERT INTO proyecto 
            (id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, presupuesto, estado)
            VALUES 
            (:id_proyecto, :nombre, :descripcion, :fecha_inicio, :fecha_fin, :presupuesto, :estado)
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "id_proyecto": proyecto.id_proyecto,
                        "nombre": proyecto.nombre,
                        "descripcion": proyecto.descripcion,
                        "fecha_inicio": proyecto.fecha_inicio,
                        "fecha_fin": proyecto.fecha_fin,
                        "presupuesto": proyecto.presupuesto,
                        "estado": proyecto.estado
                    })
                    conn.commit()
                    print(f"✓ Proyecto '{proyecto.nombre}' creado exitosamente.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: El proyecto ya existe.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error de base de datos: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_proyecto: int) -> Optional[Proyecto]:
        """Lee un proyecto por su ID"""
        sql = "SELECT * FROM proyecto WHERE id_proyecto = :id_proyecto"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_proyecto": id_proyecto})
                    row = cursor.fetchone()
                    
                    if not row:
                        print(f"✗ No se encontró proyecto con ID {id_proyecto}")
                        return None
                    
                    return ProyectoDAO._row_to_proyecto(row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer proyecto: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Proyecto]:
        """Lee todos los proyectos"""
        sql = f"SELECT * FROM proyecto FETCH FIRST {limit} ROWS ONLY"
        proyectos = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    
                    for row in cursor:
                        proyectos.append(ProyectoDAO._row_to_proyecto(row))
                    
                    print(f"✓ Se encontraron {len(proyectos)} proyecto(s).")
                    return proyectos
        except oracledb.DatabaseError as e:
            print(f"✗ Error al listar proyectos: {e}")
            raise
    
    @staticmethod
    def update(proyecto: Proyecto) -> bool:
        """Actualiza un proyecto existente"""
        sql = """
            UPDATE proyecto 
            SET nombre = :nombre,
                descripcion = :descripcion,
                fecha_inicio = :fecha_inicio,
                fecha_fin = :fecha_fin,
                presupuesto = :presupuesto,
                estado = :estado
            WHERE id_proyecto = :id_proyecto
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "nombre": proyecto.nombre,
                        "descripcion": proyecto.descripcion,
                        "fecha_inicio": proyecto.fecha_inicio,
                        "fecha_fin": proyecto.fecha_fin,
                        "presupuesto": proyecto.presupuesto,
                        "estado": proyecto.estado,
                        "id_proyecto": proyecto.id_proyecto
                    })
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró proyecto con ID {proyecto.id_proyecto}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Proyecto ID {proyecto.id_proyecto} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error al actualizar proyecto: {e}")
            raise
    
    @staticmethod
    def delete(id_proyecto: int) -> bool:
        """Elimina un proyecto por su ID"""
        sql = "DELETE FROM proyecto WHERE id_proyecto = :id_proyecto"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_proyecto": id_proyecto})
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró proyecto con ID {id_proyecto}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Proyecto ID {id_proyecto} eliminado.")
                    return True
        except oracledb.IntegrityError:
            print(f"✗ Error: No se puede eliminar el proyecto porque tiene registros asociados.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error al eliminar proyecto: {e}")
            raise
    
    @staticmethod
    def _row_to_proyecto(row) -> Proyecto:
        """Convierte una fila de la BD a objeto Proyecto"""
        (id_proy, nombre, descripcion, fecha_inicio, 
         fecha_fin, presupuesto, estado) = row
        
        return Proyecto(
            id_proyecto=id_proy,
            nombre=nombre,
            descripcion=descripcion if descripcion else "",
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            presupuesto=float(presupuesto) if presupuesto else 0.0,
            estado=estado
        )
    
    @staticmethod
    def create_with_sequence() -> int:
        """Obtiene el siguiente ID de la secuencia"""
        sql = "SELECT seq_proyecto.NEXTVAL FROM DUAL"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error al obtener siguiente ID: {e}")
            return -1
