
<!-- TODO: Registrar daemon  -->

-- 1. Dar permisos de ejecución
chmod +x 2_run_scrap.sh

-- 2. Registrar servicio
sudo vim /etc/systemd/system/startup-run-exec.service
sudo systemctl enable startup-run-exec.service

sudo systemctl status startup-run-exec.service         # Ver el estado del servicio
sudo systemctl disable startup-run-exec.service        # Para modificar los scripts siempre desactivar

/*
[Unit]
Description=Startup

[Service]
ExecStart=/home/brew_test_gcp_01/Desktop/runscrap/dependencias/2_run_scrap.sh

[Install]
WantedBy=multi-user.target
*/


-- 3. Comandos utiles
ps uax | grep python3                                # Ver si corrió el servicio
setxkbmap -layout latam                              # Cambiara a teclado latam

e.g.: ubuntu   18405  0.5  3.3 1133080 267412 pts/0  S    02:19   0:01 python3 main.py
sudo kill -9 18405  # Para detener el servicio

ps aux | grep vim
sudo kill 2445
sudo rm /etc/systemd/system/.startup-run-exec.service.swp

-- Eliminar papelera
su -
cd ~/.local/share/Trash/*
rm -rf ~/.local/share/Trash/*

rm -rf /home/brew_test_gcp_01/.local/share/Trash/files/*

-- Verificar espacio en /temp
df -h
du -sh /tmp

-- Ejecutar en segundo plano
nohup python3 z2-ExecRenacyt.py > salida_renacyt.txt 2>&1 &
nohup python3 z3-ExecOrcid.py > salida_orcid.txt 2>&1 &

#2604 -> renacyt
#4398 -> orcid

Este comando realiza lo siguiente:
    * nohup: Ejecuta el comando que le sigue sin colgar incluso si se cierra la terminal.
    * python3 z2-ExecRenacyt.py: Ejecuta tu script Python.
    * salida.txt 2>&1: Redirige la salida estándar y de error al archivo salida.txt.
    * &: Pone el proceso en segundo plano.

-- Para detener el proceso
ps aux | grep z2-ExecRenacyt.py
kill PID_del_proceso

    *Reemplaza PID_del_proceso con el ID del proceso que obtuviste al ejecutar ps.


-- Ver la salida del segundo plano
tail -f salida.txt
