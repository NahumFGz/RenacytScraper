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

def stop_process_linux(process_name):
    try:
        # Obtener la lista de procesos que contienen el nombre especificado
        process = subprocess.Popen(['pgrep', '-f', process_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        process_ids = [int(pid) for pid in stdout.decode().split()]

        if not process_ids:
            print(f"No se encontraron procesos con el nombre '{process_name}'.")
            return

        # Detener los procesos identificados
        for pid in process_ids:
            subprocess.run(['kill', str(pid)])
        
        print(f"Procesos con el nombre '{process_name}' detenidos correctamente.")
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
                stop_process_linux(process_name="java")
                #stop_process_linux(process_name="chrome")
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