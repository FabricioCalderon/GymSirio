from cx_Freeze import setup, Executable
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio base del proyecto

# Archivos y carpetas a incluir
include_files = []

db_path = os.path.join(base_dir, "manage.py")
if os.path.exists(db_path):
    include_files.append((db_path, "manage.py"))

# Base de datos SQLite
db_path = os.path.join(base_dir, "db.sqlite3")
if os.path.exists(db_path):
    include_files.append((db_path, "db.sqlite3"))

# Configuración del proyecto
settings_path = os.path.join(base_dir, "Proyecto", "settings.py")
if os.path.exists(settings_path):
    include_files.append((settings_path, "Proyecto/settings.py"))

# Carpeta "static"
static_dir = os.path.join(base_dir, "static")
if os.path.exists(static_dir):
    include_files.append((static_dir, "static"))

# Carpeta "migrations" de Aplicacion1
migrations_dir = os.path.join(base_dir, "Aplicacion1", "migrations")
if os.path.exists(migrations_dir):
    include_files.append((migrations_dir, "Aplicacion1/migrations"))

# Opciones de compilación
build_exe_options = {
    "packages": [
        "django",
        "Proyecto",
        "Aplicacion1",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.db.backends.sqlite3",  # Asegura el backend SQLite
        "django_bootstrap5",
    ],
    "includes": [
        "asyncio",
        "sqlparse",
        "jinja2.ext",
        "colorama",
        "django.utils.autoreload",
        "django.forms",
        "django_bootstrap5",
    ],
    "excludes": ["tkinter"],  # Excluir módulos innecesarios
    "include_files": include_files,
}

# Determinar si es una app de consola o GUI
base = "Console" if sys.platform == "win32" else None

setup(
    name="miProyecto",
    version="1.0",
    description="Proyecto Django ejecutable",
    options={"build_exe": build_exe_options},
    executables=[Executable("SirioGym.py", base=base)]
)
