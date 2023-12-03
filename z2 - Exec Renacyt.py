import os
import time
import psutil
import subprocess
from utils.paths import PROJECT_PATH

def limpiar_consola():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para Mac y Linux
        os.system('clear')

def stop_process_windows(process_name="java.exe"):
    for proc in psutil.process_iter():
        try:
            if proc.name() == process_name:
                proc.kill()
                print(f"Proceso {process_name} terminado correctamente.")
        except psutil.AccessDenied:
            print(f"No se tiene acceso para terminar el proceso {process_name}.")
        except psutil.NoSuchProcess:
            print(f"No se encontró el proceso {process_name}.")

def stop_java_linux():
    try:
        # Obtener la lista de procesos que contienen "java" en su nombre
        process = subprocess.Popen(['pgrep', '-f', 'java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        java_process_ids = [int(pid) for pid in stdout.decode().split()]

        if not java_process_ids:
            print("No se encontraron procesos con el nombre 'java'.")
            return

        # Detener los procesos identificados
        for pid in java_process_ids:
            subprocess.run(['kill', str(pid)])
        
        print("Procesos con el nombre 'java' detenidos correctamente.")
    except Exception as e:
        print(f"Se produjo un error al detener los procesos: {e}")


if __name__ == "__main__":
    for i in range(3000):
    # while True:
        print('i --->',str(i))

        try:
            if os.name == 'nt':
                stop_process_windows(process_name="java.exe")
                stop_process_windows(process_name="chrome.exe")
            else:
                stop_java_linux()
        except:
            pass

        try:
            if os.name == 'nt':
                os.system(f'python {PROJECT_PATH}/y2-PerfilRenacyt.py')
            else:
                os.system(f'python3 {PROJECT_PATH}/y2-PerfilRenacyt.py')
        except:
            print("Error en BoletasConsumo.py")
        
        # Eliminar los archivos bmp.log y server.log
        try:
            os.remove('bmp.log')
            os.remove('server.log')
            print("Se eliminaron los archivos bmp.log y server.log")
        except:
            pass

        limpiar_consola()