import os
import shutil
import subprocess
import sys

def run_setup_install():
    print("Reinstalando el paquete usando setup.py con --force-reinstall...")
    try:
        subprocess.check_call([sys.executable, "setup.py", "install"])
        print("Reinstalación completada.")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la instalación: {e}")
        sys.exit(1)


folders_to_clean = [
    'build',
    'dist',
    'pycrgba.egg-info',
    '__pycache__'
]


def remove_folder(folder):
    if os.path.exists(folder):
        print(f"Eliminando {folder}...")
        shutil.rmtree(folder, ignore_errors=True)
    else:
        print(f"{folder} no existe, saltando...")


def clean_up():
    print("Iniciando limpieza post-instalación...")
    for folder in folders_to_clean:
        remove_folder(folder)
    print("Limpieza completada.")


if __name__ == "__main__":
    run_setup_install()
    clean_up()
