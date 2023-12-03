####################################
## A. Librerias
####################################
import os
import time
import json

import datetime
import pandas as pd

from utils.utils import *
from utils.paths import CHROMEDRIVER_PATH, PROJECT_PATH

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

####################################
## B. Funciones
####################################

def get_files(path, extension):
    dir_name  = os.path.join(os.getcwd(), path)
    files     = os.listdir(dir_name)
    
    paths    = []
    for file in files:
        if extension in file:
            paths.append(os.path.join(path,file))

    return paths

def start_har(proxy, name):
    options = {
        'captureHeaders': True, 
        'captureContent': True, 
        'captureBinaryContent': True, 
        'captureCookies': True, 
        'captureHeadersSize': -1, 
        'captureMaxSize': -1, 
        'captureBinaryContentMaxLength': -1 # Tamaño máximo del contenido binario
    }
    proxy.new_har(name, options=options)

def format_json(dir_path):
    file_paths = get_files(dir_path, '.json')
    
    for file_path in file_paths:
        # Leer el json
        with open(file_path, 'r') as file:
            # Leer como una lista de lineas
            data = file.readlines()

            # Se agrega el corchete al inicio y al final
            data[0] = '[' + data[0]
            data[-1] = data[-1] + ']'
        
        # Escribir el json
        file_path = file_path.replace('1_datos_investigador', '2_datos_investigador_format')
        with open(file_path, 'w') as file:
            file.writelines(data)

def clean_dir(dir_name):
    try:
        files = get_files(os.path.join(os.getcwd(),'outputs','jsons',dir_name), '.')
        for file in files:
            os.remove(file)
        print('Se eliminaron los archivos de la carpeta {}'.format(dir_name))
    except:
        pass

# 4. Eliminar los archivos bmp.log y server.log
def clean_logs():
    try:
        os.remove('bmp.log')
        os.remove('server.log')
        print('Se eliminaron los archivos bmp.log y server.log')
    except:
        pass


########################
## C. Ejecución
########################

# 1. Seleccionar modo
HEADLESS = True
PRINT_VIEW = False

# 2. Eliminar todos los archivos de la carpeta
clean_dir(os.path.join(os.getcwd(),'originals','renacyt','perfil','0_json'))
clean_dir(os.path.join(os.getcwd(),'originals','renacyt','perfil','1_datos_investigador'))
clean_dir(os.path.join(os.getcwd(),'originals','renacyt','perfil','2_datos_investigador_format'))


######################
## D. Leer los jsons
######################

# 1. Leer los jsons y guardarlos en un dataframe
df_renacyt= pd.read_parquet(os.path.join(os.getcwd(),'processed','parquet','01_lista_investigadores_renacyt.parquet'))
df_renacyt = df_renacyt[df_renacyt['ctiVitae'].notnull()]
df_renacyt = df_renacyt[df_renacyt['ctiVitae'] != 'nan']
df_renacyt = df_renacyt[df_renacyt['ctiVitae'] != 'None']
df_renacyt = df_renacyt[df_renacyt['ctiVitae'] != '']
df_renacyt['ctiVitae'] = df_renacyt['ctiVitae'].astype(str)
df_renacyt.drop_duplicates(subset=['ctiVitae'], inplace=True)
df_renacyt = df_renacyt.astype(str)

# 2. Seleccionar la columna ctiVitae y crear otra columna con el url + ctiVitae
df_renacyt['url'] = 'https://ctivitae.concytec.gob.pe/buscador-ui/#/ficha/ficha-renacyt?idInvestigador=' + df_renacyt['ctiVitae']
df_renacyt = df_renacyt[['ctiVitae','orcid','url']]

df_renacyt = df_renacyt.head(3)
df_renacyt


######################
## E. Ejecutar
######################

# 1. Iterar sobre las urls
i = 0
for cti_vitae,orcid, url in df_renacyt.values.tolist(): 
    try:
        # A. Obtener el driver
        driver, server, proxy = get_chrome_driver(chromedriver_path=CHROMEDRIVER_PATH, print_view=PRINT_VIEW, headless=HEADLESS)

        # B. Iniciar har
        start_har(proxy, 'renacyt_profile')
        
        # C. Ingresar a la URL y esperar a que la tabla específica esté presente en el DOM
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        table_locator = (By.CSS_SELECTOR, 'table.table.table-sm')
        table = wait.until(EC.presence_of_element_located(table_locator))
        print(f'{i}. {url}')

        # D. Obtener el har
        time.sleep(4)
        har = proxy.har

        # E. Guardar json original
        j = 0
        k = 0
        for entrie in har.get('log').get('entries'):

            # JSON original
            data_list = str(entrie)
            with open(os.path.join(os.getcwd(),'originals','renacyt','perfil','0_json', str(i) + 'x' + str(j) + '.json'), 'w') as json_file:
                json.dump(data_list, json_file, indent=4)
                j += 1

            # Datos del investigador
            string_content = entrie.get('response').get('content').get('text')
            if '"formacionesAcademicas"' in str(string_content):
                data_list = json.loads(string_content)
                with open(os.path.join(os.getcwd(),'originals','renacyt','perfil','1_datos_investigador'
                                       , str(i) + 'x' + str(k) 
                                       + '_' + str(cti_vitae)
                                       + '_' + str(orcid) +'_.json'), 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
                    k += 1

        # F. Finalizar driver, server, proxy y eliminar los logs
        stop_chrome_driver(driver, server, proxy)
        clean_logs()

        # G. Actualizar el contador
        i += 1
        print('')

    except:
        pass


# 2. Formatear los jsons
format_json(os.path.join(os.getcwd(),'originals','renacyt','perfil','1_datos_investigador'))