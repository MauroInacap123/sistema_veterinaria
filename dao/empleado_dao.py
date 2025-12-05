"""
Módulo: dao/empleado_dao.py
Data Access Object para la entidad Empleado
"""

import oracledb
from typing import List, Optional
from datetime import datetime
from models.empleado import Empleado
from database import get_connection


class EmpleadoDAO:
    """Clase para manejar operaciones CRUD de Empleado"""
    
    @staticmethod
    def create(empleado: Empleado) -> bool:
        """Crea un nuevo empleado en la base de datos"""
        sql = """
            INSERT INTO empleado 
            (id_empleado, rut, nombres, apellidos, email, telefono, 
             fecha_contratacion, salario, id_departamento)
            VALUES 
            (:id_empleado, :rut, :nombres, :apellidos, :email, :telefono,
             :fecha_contratacion, :salario, :id_departamento)
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "id_empleado": empleado.id_empleado,
                        "rut": empleado.rut,
                        "nombres": empleado.nombres,
                        "apellidos": empleado.apellidos,
                        "email": empleado.email,
                        "telefono": empleado.telefono,
                        "fecha_contratacion": empleado.fecha_contratacion,
                        "salario": empleado.salario,
                        "id_departamento": empleado.id_departamento
                    })
                    conn.commit()
                    print(f"✓ Empleado '{empleado.obtener_nombre_completo()}' creado exitosamente.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: El empleado ya existe o hay un problema de integridad.")
            print(f"   Detalles: {e}")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error de base de datos: {e}")
            raise
    
    @staticmethod
    def read_by_id(id_empleado: int) -> Optional[Empleado]:
        """Lee un empleado por su ID"""
        sql = "SELECT * FROM empleado WHERE id_empleado = :id_empleado"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_empleado": id_empleado})
                    row = cursor.fetchone()
                    
                    if not row:
                        print(f"✗ No se encontró empleado con ID {id_empleado}")
                        return None
                    
                    return EmpleadoDAO._row_to_empleado(row)
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer empleado: {e}")
            raise
    
    @staticmethod
    def read_all(limit: int = 100) -> List[Empleado]:
        """Lee todos los empleados"""
        sql = f"SELECT * FROM empleado FETCH FIRST {limit} ROWS ONLY"
        empleados = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    
                    for row in cursor:
                        empleados.append(EmpleadoDAO._row_to_empleado(row))
                    
                    print(f"✓ Se encontraron {len(empleados)} empleado(s).")
                    return empleados
        except oracledb.DatabaseError as e:
            print(f"✗ Error al listar empleados: {e}")
            raise
    
    @staticmethod
    def update(empleado: Empleado) -> bool:
        """Actualiza un empleado existente"""
        sql = """
            UPDATE empleado 
            SET rut = :rut,
                nombres = :nombres,
                apellidos = :apellidos,
                email = :email,
                telefono = :telefono,
                fecha_contratacion = :fecha_contratacion,
                salario = :salario,
                id_departamento = :id_departamento
            WHERE id_empleado = :id_empleado
        """
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {
                        "rut": empleado.rut,
                        "nombres": empleado.nombres,
                        "apellidos": empleado.apellidos,
                        "email": empleado.email,
                        "telefono": empleado.telefono,
                        "fecha_contratacion": empleado.fecha_contratacion,
                        "salario": empleado.salario,
                        "id_departamento": empleado.id_departamento,
                        "id_empleado": empleado.id_empleado
                    })
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró empleado con ID {empleado.id_empleado}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Empleado ID {empleado.id_empleado} actualizado.")
                    return True
        except oracledb.DatabaseError as e:
            print(f"✗ Error al actualizar empleado: {e}")
            raise
    
    @staticmethod
    def delete(id_empleado: int) -> bool:
        """Elimina un empleado por su ID"""
        sql = "DELETE FROM empleado WHERE id_empleado = :id_empleado"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_empleado": id_empleado})
                    
                    if cursor.rowcount == 0:
                        print(f"✗ No se encontró empleado con ID {id_empleado}")
                        return False
                    
                    conn.commit()
                    print(f"✓ Empleado ID {id_empleado} eliminado.")
                    return True
        except oracledb.IntegrityError as e:
            print(f"✗ Error: No se puede eliminar el empleado porque tiene registros asociados.")
            return False
        except oracledb.DatabaseError as e:
            print(f"✗ Error al eliminar empleado: {e}")
            raise
    
    @staticmethod
    def read_by_departamento(id_departamento: int) -> List[Empleado]:
        """Lee todos los empleados de un departamento"""
        sql = "SELECT * FROM empleado WHERE id_departamento = :id_departamento"
        empleados = []
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"id_departamento": id_departamento})
                    
                    for row in cursor:
                        empleados.append(EmpleadoDAO._row_to_empleado(row))
                    
                    return empleados
        except oracledb.DatabaseError as e:
            print(f"✗ Error al leer empleados por departamento: {e}")
            raise
    
    @staticmethod
    def _row_to_empleado(row) -> Empleado:
        """Convierte una fila de la BD a objeto Empleado"""
        (id_emp, rut, nombres, apellidos, email, telefono, 
         fecha_contratacion, salario, id_dep) = row
        
        return Empleado(
            id_empleado=id_emp,
            rut=rut,
            nombres=nombres,
            apellidos=apellidos,
            email=email if email else "",
            telefono=telefono if telefono else "",
            fecha_contratacion=fecha_contratacion,
            salario=float(salario),
            id_departamento=id_dep
        )
    
    @staticmethod
    def create_with_sequence() -> int:
        """Obtiene el siguiente ID de la secuencia"""
        sql = "SELECT seq_empleado.NEXTVAL FROM DUAL"
        
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    return cursor.fetchone()[0]
        except oracledb.DatabaseError as e:
            print(f"✗ Error al obtener siguiente ID: {e}")
            return -1
