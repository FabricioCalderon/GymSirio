import os
import sys
import django
import subprocess
import time
import webbrowser
from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proyecto.settings")
    django.setup()

    print("Aplicando migraciones...")
    execute_from_command_line(["Proyecto/manage.py", "makemigrations", "--noinput"])
    execute_from_command_line(["Proyecto/manage.py", "migrate", "--noinput"])
    print("Migraciones aplicadas correctamente.")

    User = get_user_model()
    superuser_username = "sirio"

    if not User.objects.filter(username=superuser_username).exists():
        User.objects.create_superuser(superuser_username, "admin@example.com", "sirio123")
        print("Superusuario creado.")
    else:
        print("El superusuario ya existe, no se creó uno nuevo.")

    print("Iniciando servidor Django...")

    # print("Servidor iniciado en http://127.0.0.1:8000/")
    webbrowser.open("http://127.0.0.1:8000/")

    # Ejecuta el comando 'runserver' automáticamente
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000"])

#  # 🔹 Ejecuta el servidor en segundo plano
#     server = subprocess.Popen(
#         [sys.executable, "Proyecto/manage.py", "runserver", "127.0.0.1:8000"],
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         creationflags=subprocess.DETACHED_PROCESS  # IMPORTANTE: Mantiene el servidor vivo tras cerrar la consola
#     )

#     # 🔹 Esperar un momento para que arranque el servidor
#     time.sleep(3)

#     # 🔹 Intentar abrir el navegador hasta que el servidor esté listo
#     max_retries = 10
#     for i in range(max_retries):
#         try:
#             webbrowser.open("http://127.0.0.1:8000/")
#             print("✅ Navegador abierto correctamente.")
#             break
#         except:
#             time.sleep(1)

#     # 🔹 Cerrar la consola sin matar el servidor
#     sys.exit()
