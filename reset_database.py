"""
Script para borrar y recrear la base de datos
Uso: python reset_database.py
"""
import os
import sys

# Añadir el directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.core.database import engine, Base
from api.core.models import UserDB, Customer, Pet, Appointment, Doctor

def reset_database():
    """Borra y recrea todas las tablas de la base de datos"""

    # Ruta del archivo de base de datos
    db_path = os.path.join(os.path.dirname(__file__), "api", "core", "customers.sqlite")

    print("=" * 50)
    print("RESETEAR BASE DE DATOS")
    print("=" * 50)

    # Verificar si existe la base de datos
    if os.path.exists(db_path):
        print(f"\n✓ Base de datos encontrada: {db_path}")
        respuesta = input("\n¿Estás seguro de que quieres borrar la base de datos? (si/no): ")

        if respuesta.lower() not in ['si', 's', 'yes', 'y']:
            print("\n❌ Operación cancelada")
            return

        # Borrar todas las tablas
        print("\n🗑️  Borrando todas las tablas...")
        Base.metadata.drop_all(bind=engine)
        print("✓ Tablas borradas exitosamente")
    else:
        print(f"\nℹ️  No se encontró base de datos existente")

    # Crear todas las tablas nuevamente
    print("\n🔨 Creando todas las tablas nuevamente...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente")

    print("\n" + "=" * 50)
    print("✅ BASE DE DATOS RESETEADA CORRECTAMENTE")
    print("=" * 50)
    print("\nTablas creadas:")
    print("  - users")
    print("  - customers")
    print("  - pets")
    print("  - appointments")
    print("  - doctors")
    print()

if __name__ == "__main__":
    reset_database()
