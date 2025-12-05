"""
Módulo: dao/departamento_dao.py
Data Access Object para la entidad Departamento
Maneja todas las operaciones CRUD con la base de datos
"""

import oracledb
from typing import List, Optional
from models.departamento import Departamento
from database import get_connection


class DepartamentoDAO:
    """Clase para manejar operaciones CRUD de Departamento"""
    
    @staticmethod
    def create(departamento: Departamento) -> bool:
        """
        Crea un nuevo departamento en la base de datos
        
        Args:
            departamento: Objeto Departamento a crear
            
        Returns:
            bool: True si se creó exitosamente
            
        Raises:
            oracledb.DatabaseError: Si hay error en la BD
        """
        sql = """
            INSERT INTO departamento (id_departamento, nombre, ubicacion, presupuesto)
            VALUES (:id_departamento, :nombre, :ubicacion, :presupuesto)
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "id_departamento": departamento.id_departamento,
                        "nombre": departamento.nombre,
                        "ubicacion": departamento.ubicacion,
                        "presupuesto": departamento.presupuesto
                    })
                    conn.commit()
                    print(f"✓ Departamento '{departamento.nombre}' creado exitosamente.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: El departamento ya existe o hay un problema de integridad.")
            print(f"   Detalles: {e}")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error de base de datos al crear departamento: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_departamento: int) -> Optional[Departamento]:
        """
        Lee un departamento por su ID
        
        Args:
            id_departamento: ID del departamento a buscar
            
        Returns:
            Departamento: Objeto Departamento o None si no existe
        """
        sql = "SELECT * FROM departamento WHERE id_departamento = :id_departamento"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_departamento": id_departamento})
                    row = cursor.fetchone()
                    
                    if not row:
                        print(f"✗ No se encontró departamento con ID {id_departamento}")
                        return None
                    
                    # Desempaquetar la fila
                    id_dep, nombre, ubicacion, presupuesto = row
                    
                    return Departamento(
                        id_departamento=id_dep,
                        nombre=nombre,
                        ubicacion=ubicacion,
                        presupuesto=float(presupuesto) if presupuesto else 0.0
                    )
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer departamento: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Departamento]:
        """
        Lee todos los departamentos
        
        Args:
            limit: Límite de registros a retornar
            
        Returns:
            List[Departamento]: Lista de departamentos
        """
        sql = f"SELECT * FROM departamento FETCH FIRST {limit} ROWS ONLY"
        departamentos = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    
                    for row in cursor:
                        id_dep, nombre, ubicacion, presupuesto = row
                        dept = Departamento(
                            id_departamento=id_dep,
                            nombre=nombre,
                            ubicacion=ubicacion,
                            presupuesto=float(presupuesto) if presupuesto else 0.0
                        )
                        departamentos.append(dept)
                    
                    print(f"✓ Se encontraron {len(departamentos)} departamento(s).")
                    return departamentos
        except oracledb.DatabaseError as e:
            print(f"✗ Error al listar departamentos: {e}")
            raise
    
    @staticmethod
    def update(departamento: Departamento) -> bool:
        """
        Actualiza un departamento existente
        
        Args:
            departamento: Objeto Departamento con los datos actualizados
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        sql = """
            UPDATE departamento 
            SET nombre = :nombre,
                ubicacion = :ubicacion,
                presupuesto = :presupuesto
            WHERE id_departamento = :id_departamento
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "nombre": departamento.nombre,
                        "ubicacion": departamento.ubicacion,
                        "presupuesto": departamento.presupuesto,
                        "id_departamento": departamento.id_departamento
                    })
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró departamento con ID {departamento.id_departamento}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Departamento ID {departamento.id_departamento} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error al actualizar departamento: {e}")
            raise
    
    @staticmethod
    def delete(id_departamento: int) -> bool:
        """
        Elimina un departamento por su ID
        
        Args:
            id_departamento: ID del departamento a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        sql = "DELETE FROM departamento WHERE id_departamento = :id_departamento"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_departamento": id_departamento})
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró departamento con ID {id_departamento}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Departamento ID {id_departamento} eliminado.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: No se puede eliminar el departamento porque tiene empleados asignados.")
            print(f"   Detalles: {e}")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error al eliminar departamento: {e}")
            raise
    
    @staticmethod
    def create_with_sequence() -> int:
        """
        Crea un nuevo departamento usando la secuencia de Oracle
        para generar el ID automáticamente
        
        Returns:
            int: ID del nuevo departamento o -1 si hay error
        """
        sql = "SELECT seq_departamento.NEXTVAL FROM DUAL"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    nuevo_id = cursor.fetchone()[0]
                    return nuevo_id
        except oracledb.DatabaseError as e:
            print(f"✗ Error al obtener siguiente ID: {e}")
            return -1
