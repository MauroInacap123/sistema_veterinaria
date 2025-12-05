"""
Sistema de Gestión Veterinaria
Aplicación principal con menús CRUD
Mauricio Bustamante - INACAP
"""

import os
from datetime import datetime, date
from database import test_connection
from dao import ClienteDAO, MascotaDAO, VeterinarioDAO, CitaDAO
from models import Cliente, Mascota, Veterinario, Cita


def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo"""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución hasta que el usuario presione ENTER"""
    input("\nPresione ENTER para continuar...")


# ============================================
# MENÚ CRUD: CLIENTES
# ============================================

def menu_clientes():
    """Menú CRUD para gestión de clientes"""
    while True:
        limpiar_pantalla()
        print("""
        ====================================
        |       GESTIÓN: CLIENTES          |
        |----------------------------------|
        | 1. Crear cliente                 |
        | 2. Listar todos los clientes     |
        | 3. Buscar cliente por ID         |
        | 4. Actualizar cliente            |
        | 5. Eliminar cliente              |
        | 0. Volver al menú principal      |
        ====================================
        """)
        
        opcion = input("Elige una opción [1-5, 0]: ")
        
        if opcion == "1":
            limpiar_pantalla()
            print("=== CREAR CLIENTE ===\n")
            try:
                nuevo_id = ClienteDAO.create_with_sequence()
                rut = input("RUT (ej: 12345678-9): ")
                nombres = input("Nombres: ")
                apellidos = input("Apellidos: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                direccion = input("Dirección: ")
                
                cliente = Cliente(nuevo_id, rut, nombres, apellidos, telefono, email, direccion)
                ClienteDAO.create(cliente)
            except ValueError as e:
                print(f"✗ Error de validación: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=== LISTADO DE CLIENTES ===\n")
            try:
                clientes = ClienteDAO.read_all()
                if clientes:
                    for cli in clientes:
                        print(f"  {cli}")
                else:
                    print("No hay clientes registrados.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=== BUSCAR CLIENTE ===\n")
            try:
                id_cli = int(input("ID del cliente: "))
                cli = ClienteDAO.read_by_id(id_cli)
                if cli:
                    print(f"\n{cli}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=== ACTUALIZAR CLIENTE ===\n")
            try:
                id_cli = int(input("ID del cliente a actualizar: "))
                cli = ClienteDAO.read_by_id(id_cli)
                
                if cli:
                    print(f"\nDatos actuales: {cli}\n")
                    print("Ingrese los nuevos datos (Enter para mantener):")
                    
                    rut = input(f"RUT [{cli.rut}]: ") or cli.rut
                    nombres = input(f"Nombres [{cli.nombres}]: ") or cli.nombres
                    apellidos = input(f"Apellidos [{cli.apellidos}]: ") or cli.apellidos
                    telefono = input(f"Teléfono [{cli.telefono}]: ") or cli.telefono
                    email = input(f"Email [{cli.email}]: ") or cli.email
                    direccion = input(f"Dirección [{cli.direccion}]: ") or cli.direccion
                    
                    cli.rut = rut
                    cli.nombres = nombres
                    cli.apellidos = apellidos
                    cli.telefono = telefono
                    cli.email = email
                    cli.direccion = direccion
                    
                    ClienteDAO.update(cli)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=== ELIMINAR CLIENTE ===\n")
            try:
                id_cli = int(input("ID del cliente a eliminar: "))
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == "s":
                    ClienteDAO.delete(id_cli)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("✗ Opción incorrecta.")
            pausar()


# ============================================
# MENÚ CRUD: MASCOTAS
# ============================================

def menu_mascotas():
    """Menú CRUD para gestión de mascotas"""
    while True:
        limpiar_pantalla()
        print("""
        ====================================
        |       GESTIÓN: MASCOTAS          |
        |----------------------------------|
        | 1. Crear mascota                 |
        | 2. Listar todas las mascotas     |
        | 3. Buscar mascota por ID         |
        | 4. Actualizar mascota            |
        | 5. Eliminar mascota              |
        | 6. Listar mascotas por cliente   |
        | 0. Volver al menú principal      |
        ====================================
        """)
        
        opcion = input("Elige una opción [1-6, 0]: ")
        
        if opcion == "1":
            limpiar_pantalla()
            print("=== CREAR MASCOTA ===\n")
            try:
                nuevo_id = MascotaDAO.create_with_sequence()
                nombre = input("Nombre: ")
                print("Especies: PERRO, GATO, AVE, CONEJO, HAMSTER")
                especie = input("Especie: ").upper()
                raza = input("Raza: ")
                edad = int(input("Edad (años): "))
                color = input("Color: ")
                peso = float(input("Peso (kg): "))
                id_cliente = int(input("ID del dueño (cliente): "))
                
                mascota = Mascota(nuevo_id, nombre, especie, raza, edad, color, peso, id_cliente)
                MascotaDAO.create(mascota)
            except ValueError as e:
                print(f"✗ Error de validación: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=== LISTADO DE MASCOTAS ===\n")
            try:
                mascotas = MascotaDAO.read_all()
                if mascotas:
                    for masc in mascotas:
                        print(f"  {masc}")
                        if masc.es_cachorro():
                            print("    → Es cachorro")
                        if masc.es_senior():
                            print("    → Es senior")
                else:
                    print("No hay mascotas registradas.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=== BUSCAR MASCOTA ===\n")
            try:
                id_masc = int(input("ID de la mascota: "))
                masc = MascotaDAO.read_by_id(id_masc)
                if masc:
                    print(f"\n{masc}")
                    print(f"Cachorro: {'Sí' if masc.es_cachorro() else 'No'}")
                    print(f"Senior: {'Sí' if masc.es_senior() else 'No'}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=== ACTUALIZAR MASCOTA ===\n")
            try:
                id_masc = int(input("ID de la mascota a actualizar: "))
                masc = MascotaDAO.read_by_id(id_masc)
                
                if masc:
                    print(f"\nDatos actuales: {masc}\n")
                    print("Ingrese los nuevos datos (Enter para mantener):")
                    
                    nombre = input(f"Nombre [{masc.nombre}]: ") or masc.nombre
                    edad_str = input(f"Edad [{masc.edad}]: ")
                    edad = int(edad_str) if edad_str else masc.edad
                    peso_str = input(f"Peso [{masc.peso}]: ")
                    peso = float(peso_str) if peso_str else masc.peso
                    
                    masc.nombre = nombre
                    masc.edad = edad
                    masc.peso = peso
                    
                    MascotaDAO.update(masc)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=== ELIMINAR MASCOTA ===\n")
            try:
                id_masc = int(input("ID de la mascota a eliminar: "))
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == "s":
                    MascotaDAO.delete(id_masc)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "6":
            limpiar_pantalla()
            print("=== MASCOTAS POR CLIENTE ===\n")
            try:
                id_cli = int(input("ID del cliente: "))
                mascotas = MascotaDAO.read_by_cliente(id_cli)
                if mascotas:
                    print(f"\nMascotas del cliente {id_cli}:")
                    for masc in mascotas:
                        print(f"  {masc}")
                else:
                    print("El cliente no tiene mascotas registradas.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("✗ Opción incorrecta.")
            pausar()


# ============================================
# MENÚ CRUD: VETERINARIOS
# ============================================

def menu_veterinarios():
    """Menú CRUD para gestión de veterinarios"""
    while True:
        limpiar_pantalla()
        print("""
        ====================================
        |     GESTIÓN: VETERINARIOS        |
        |----------------------------------|
        | 1. Crear veterinario             |
        | 2. Listar todos los veterinarios |
        | 3. Buscar veterinario por ID     |
        | 4. Actualizar veterinario        |
        | 5. Eliminar veterinario          |
        | 0. Volver al menú principal      |
        ====================================
        """)
        
        opcion = input("Elige una opción [1-5, 0]: ")
        
        if opcion == "1":
            limpiar_pantalla()
            print("=== CREAR VETERINARIO ===\n")
            try:
                nuevo_id = VeterinarioDAO.create_with_sequence()
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                especialidad = input("Especialidad: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                
                vet = Veterinario(nuevo_id, nombre, apellido, especialidad, telefono, email)
                VeterinarioDAO.create(vet)
            except ValueError as e:
                print(f"✗ Error de validación: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=== LISTADO DE VETERINARIOS ===\n")
            try:
                vets = VeterinarioDAO.read_all()
                if vets:
                    for vet in vets:
                        print(f"  {vet}")
                else:
                    print("No hay veterinarios registrados.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=== BUSCAR VETERINARIO ===\n")
            try:
                id_vet = int(input("ID del veterinario: "))
                vet = VeterinarioDAO.read_by_id(id_vet)
                if vet:
                    print(f"\n{vet}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=== ACTUALIZAR VETERINARIO ===\n")
            try:
                id_vet = int(input("ID del veterinario a actualizar: "))
                vet = VeterinarioDAO.read_by_id(id_vet)
                
                if vet:
                    print(f"\nDatos actuales: {vet}\n")
                    print("Ingrese los nuevos datos (Enter para mantener):")
                    
                    nombre = input(f"Nombre [{vet.nombre}]: ") or vet.nombre
                    apellido = input(f"Apellido [{vet.apellido}]: ") or vet.apellido
                    especialidad = input(f"Especialidad [{vet.especialidad}]: ") or vet.especialidad
                    telefono = input(f"Teléfono [{vet.telefono}]: ") or vet.telefono
                    email = input(f"Email [{vet.email}]: ") or vet.email
                    
                    vet.nombre = nombre
                    vet.apellido = apellido
                    vet.especialidad = especialidad
                    vet.telefono = telefono
                    vet.email = email
                    
                    VeterinarioDAO.update(vet)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=== ELIMINAR VETERINARIO ===\n")
            try:
                id_vet = int(input("ID del veterinario a eliminar: "))
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == "s":
                    VeterinarioDAO.delete(id_vet)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("✗ Opción incorrecta.")
            pausar()


# ============================================
# MENÚ CRUD: CITAS
# ============================================

def menu_citas():
    """Menú CRUD para gestión de citas"""
    while True:
        limpiar_pantalla()
        print("""
        ====================================
        |         GESTIÓN: CITAS           |
        |----------------------------------|
        | 1. Crear cita                    |
        | 2. Listar todas las citas        |
        | 3. Buscar cita por ID            |
        | 4. Citas por mascota             |
        | 5. Citas por veterinario         |
        | 6. Actualizar cita               |
        | 7. Eliminar cita                 |
        | 0. Volver al menú principal      |
        ====================================
        """)
        
        opcion = input("Elige una opción [1-7, 0]: ")
        
        if opcion == "1":
            limpiar_pantalla()
            print("=== CREAR CITA ===\n")
            try:
                nuevo_id = CitaDAO.create_with_sequence()
                id_mascota = int(input("ID de la mascota: "))
                id_vet = int(input("ID del veterinario: "))
                fecha_str = input("Fecha (YYYY-MM-DD) [hoy]: ") or datetime.now().strftime("%Y-%m-%d")
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                hora = input("Hora (ej: 10:00): ")
                motivo = input("Motivo de la consulta: ")
                print("\nEstados: PENDIENTE, CONFIRMADA, COMPLETADA, CANCELADA")
                estado = input("Estado [PENDIENTE]: ") or "PENDIENTE"
                
                cita = Cita(nuevo_id, id_mascota, id_vet, fecha, hora, motivo, estado)
                CitaDAO.create(cita)
            except ValueError as e:
                print(f"✗ Error de validación: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "2":
            limpiar_pantalla()
            print("=== LISTADO DE CITAS ===\n")
            try:
                citas = CitaDAO.read_all()
                if citas:
                    for cita in citas:
                        print(f"  {cita}")
                        if cita.motivo:
                            print(f"    Motivo: {cita.motivo[:50]}...")
                else:
                    print("No hay citas registradas.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "3":
            limpiar_pantalla()
            print("=== BUSCAR CITA ===\n")
            try:
                id_cita = int(input("ID de la cita: "))
                cita = CitaDAO.read_by_id(id_cita)
                if cita:
                    print(f"\n{cita}")
                    print(f"Motivo: {cita.motivo}")
                    if cita.diagnostico:
                        print(f"Diagnóstico: {cita.diagnostico}")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "4":
            limpiar_pantalla()
            print("=== CITAS POR MASCOTA ===\n")
            try:
                id_masc = int(input("ID de la mascota: "))
                citas = CitaDAO.read_by_mascota(id_masc)
                if citas:
                    print(f"\nCitas de la mascota {id_masc}:")
                    for cita in citas:
                        print(f"  {cita}")
                    print(f"\nTotal de citas: {len(citas)}")
                else:
                    print("La mascota no tiene citas registradas.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "5":
            limpiar_pantalla()
            print("=== CITAS POR VETERINARIO ===\n")
            try:
                id_vet = int(input("ID del veterinario: "))
                citas = CitaDAO.read_by_veterinario(id_vet)
                if citas:
                    print(f"\nCitas del veterinario {id_vet}:")
                    for cita in citas:
                        print(f"  {cita}")
                    print(f"\nTotal de citas: {len(citas)}")
                else:
                    print("El veterinario no tiene citas asignadas.")
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "6":
            limpiar_pantalla()
            print("=== ACTUALIZAR CITA ===\n")
            try:
                id_cita = int(input("ID de la cita a actualizar: "))
                cita = CitaDAO.read_by_id(id_cita)
                
                if cita:
                    print(f"\nDatos actuales: {cita}\n")
                    print("Ingrese los nuevos datos (Enter para mantener):")
                    
                    estado = input(f"Estado [{cita.estado}]: ") or cita.estado
                    diagnostico = input(f"Diagnóstico: ")
                    
                    cita.estado = estado
                    if diagnostico:
                        cita.diagnostico = diagnostico
                    
                    CitaDAO.update(cita)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "7":
            limpiar_pantalla()
            print("=== ELIMINAR CITA ===\n")
            try:
                id_cita = int(input("ID de la cita a eliminar: "))
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == "s":
                    CitaDAO.delete(id_cita)
            except Exception as e:
                print(f"✗ Error: {e}")
            pausar()
        
        elif opcion == "0":
            break
        else:
            print("✗ Opción incorrecta.")
            pausar()


# ============================================
# MENÚ PRINCIPAL
# ============================================

def main():
    """Función principal del sistema"""
    limpiar_pantalla()
    print("=" * 50)
    print("SISTEMA DE GESTIÓN VETERINARIA")
    print("Mauricio Bustamante - INACAP")
    print("=" * 50)
    print("\nProbando conexión a la base de datos...")
    
    if not test_connection():
        print("\n✗ No se pudo conectar a la base de datos.")
        print("Verifique la configuración en el archivo .env")
        pausar()
        return
    
    while True:
        limpiar_pantalla()
        print("""
        ====================================
        |  SISTEMA GESTIÓN VETERINARIA     |
        |----------------------------------|
        | 1. Gestionar Clientes            |
        | 2. Gestionar Mascotas            |
        | 3. Gestionar Veterinarios        |
        | 4. Gestionar Citas               |
        | 0. Salir del sistema             |
        ====================================
        """)
        
        opcion = input("Elige una opción [1-4, 0]: ")
        
        if opcion == "1":
            menu_clientes()
        elif opcion == "2":
            menu_mascotas()
        elif opcion == "3":
            menu_veterinarios()
        elif opcion == "4":
            menu_citas()
        elif opcion == "0":
            limpiar_pantalla()
            print("\n¡Gracias por usar el sistema!")
            print("Desarrollado por Mauricio Bustamante\n")
            break
        else:
            print("✗ Opción incorrecta.")
            pausar()


if __name__ == "__main__":
    main()
