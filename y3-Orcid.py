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

def format_json(dir_path, aux_replace_a, aux_replace_b):
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
        file_path = file_path.replace(aux_replace_a, aux_replace_b)
        with open(file_path, 'w') as file:
            file.writelines(data)


def clean_dir(dir_name):
    try:
        files = get_files(os.path.join(os.getcwd(),'outputs','jsons',dir_name), '.json')
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
clean_dir(os.path.join(os.getcwd(),'originals','orcid','0_json'))
# clean_dir(os.path.join(os.getcwd(),'originals','orcid','1_perfil'))
# clean_dir(os.path.join(os.getcwd(),'originals','orcid','2_perfil_format'))
# clean_dir(os.path.join(os.getcwd(),'originals','orcid','3_publicaciones'))
# clean_dir(os.path.join(os.getcwd(),'originals','orcid','4_publicaciones_format'))
# print("test push")

######################
## D. Leer los jsons
######################

# 1. Leer los jsons y guardarlos en un dataframe
df_orcid= pd.read_parquet(os.path.join(os.getcwd(),'processed','parquet','01_lista_investigadores_renacyt.parquet'))
df_orcid = df_orcid[df_orcid['orcid'].notnull()]
df_orcid = df_orcid[df_orcid['orcid'] != 'nan']
df_orcid = df_orcid[df_orcid['orcid'] != 'None']
df_orcid = df_orcid[df_orcid['orcid'] != '']
df_orcid['orcid'] = df_orcid['orcid'].astype(str)
df_orcid.drop_duplicates(subset=['orcid'], inplace=True)

# 2. Seleccionar la columna orcid y crear otra columna con el url + orcid
df_orcid = df_orcid[['ctiVitae','orcid']]
df_orcid['url'] = 'https://orcid.org/' + df_orcid['orcid']
print('Registros originales: ' + str(df_orcid.shape[0]))

# 3. Leer el parquet de ejecuciones
df_ejecuciones_base = pd.read_parquet(os.path.join(os.getcwd(),'originals','ejecuciones_orcid.parquet'))
df_ejecuciones_base['cti_vitae'] = df_ejecuciones_base['cti_vitae'].str.replace('_Error', '')

# 4. Obtener el maximo valor de i
df_ejecuciones_base['i'] = df_ejecuciones_base['i'].astype(int)
max_i = df_ejecuciones_base['i'].max()

if pd.isna(max_i):
    max_i = 0
else:
    max_i = max_i + 1

# 5. A df_renacyt['ctiVitae'] filtrar todos los df_ejecuciones_base['cti_vitae']
df_orcid = df_orcid[~df_orcid['ctiVitae'].isin(df_ejecuciones_base['cti_vitae'])]
print('Registros filtrados: ' + str(df_orcid.shape[0]))

df_orcid = df_orcid.head(4)
print('Registros a ejecutar: ' + str(df_orcid.shape[0]))
print('Valor de max_i: ' + str(max_i))

######################
## E. Ejecutar
######################

# 1. Iterar sobre las urls
i = max_i 
for cti_vitae,orcid, url in df_orcid.values.tolist(): 
    try:
        # A. Obtener el driver
        driver, server, proxy = get_chrome_driver(chromedriver_path=CHROMEDRIVER_PATH, print_view=PRINT_VIEW, headless=HEADLESS)

        # B. Iniciar har
        start_har(proxy, 'renacyt_profile')
        
        # C. Ingresar a la URL y esperar a que se cargue el aviso de cookies
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        table_locator = (By.ID, 'onetrust-accept-btn-handler')
        table = wait.until(EC.presence_of_element_located(table_locator))

        # D. Aceptar el aviso de cookies
        find_element_and_click(driver, 'id', 'onetrust-accept-btn-handler')
        print(f'{i}. {url}')

        # E. Obtener el har
        time.sleep(4)
        har = proxy.har

        # F. Guardar json original
        j = 0
        k = 0
        l = 0
        for entrie in har.get('log').get('entries'):

            # JSON original
            data_list = str(entrie)
            with open(os.path.join(os.getcwd(),'originals','orcid','0_json', str(i) + 'x' + str(j) + '.json'), 'w') as json_file:
                json.dump(data_list, json_file, indent=4)
                j += 1

            # Perfil
            string_content = entrie.get('response').get('content').get('text')
            if '{"title":' in str(string_content) \
                and '"assertionOriginOrcid"' in str(string_content) \
                and '"assertionOriginClientId"' in str(string_content):
                
                data_list = json.loads(string_content)
                with open(os.path.join( os.getcwd(),'originals','orcid','1_perfil'
                                        ,str(i) + 'x' + str(j) 
                                    + '_' + str(cti_vitae)
                                    + '_'+ str(orcid) +'_.json'), 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
            j += 1

            # Publicaciones
            string_content = entrie.get('response').get('content').get('text')
            if '[{"activePutCode":' in str(string_content) \
                and '"totalGroups"' in str(string_content) \
                and '"assertionOriginOrcid"' in str(string_content) \
                and '"assertionOriginClientId"' in str(string_content):

                data_list = json.loads(string_content)
                with open(os.path.join( os.getcwd(),'originals','orcid','3_publicaciones'
                                        ,str(i) + 'x' + str(l)
                                    + '_' + str(cti_vitae)
                                    + '_'+ str(orcid) +'_.json'), 'w') as json_file:
                    json.dump(data_list, json_file, indent=4)
            l+= 1

        # F. Finalizar driver, server, proxy y eliminar los logs
        stop_chrome_driver(driver, server, proxy)
        clean_dir(os.path.join(os.getcwd(),'originals','orcid','0_json'))
        
        # G. Actualizar el registro de ejecuciones_renacyt
        df_ejecuciones_base = pd.read_parquet(os.path.join(os.getcwd(),'originals','ejecuciones_orcid.parquet'))
        df_ejecuciones_actual = pd.concat([df_ejecuciones_base, pd.DataFrame({'i': [i], 'cti_vitae': [cti_vitae], 'orcid': [orcid]})], axis=0)
        df_ejecuciones_actual.to_parquet(os.path.join(os.getcwd(),'originals','ejecuciones_orcid.parquet'), index=False)

        # H. Actualizar el contador
        i += 1
    except:
        # I. Si falla guardar i, cti_vitae + '_Error' y orcid + '_Error' en un parquet
        df_ejecuciones_base = pd.read_parquet(os.path.join(os.getcwd(),'originals','ejecuciones_orcid.parquet'))
        df_ejecuciones_actual = pd.concat([df_ejecuciones_base, pd.DataFrame({'i': [i], 'cti_vitae': [cti_vitae + '_Error'], 'orcid': [orcid + '_Error']})], axis=0)
        df_ejecuciones_actual.to_parquet(os.path.join(os.getcwd(),'originals','ejecuciones_orcid.parquet'), index=False)

        # J. Actualizar el contador
        i += 1

# 2. Formatear los jsons
format_json(os.path.join(os.getcwd(),'originals','orcid','1_perfil'), '1_perfil', '2_perfil_format')
format_json(os.path.join(os.getcwd(),'originals','orcid','3_publicaciones'), '3_publicaciones', '4_publicaciones_format')