# -*- coding: utf-8 -*-
#################### для сервера
import os
listok = []

listok += [input('vvedite HOSTNAME 1-ogo (iz treh) clienta ')]
listok += [input('vvedite HOSTNAME 2-ogo (iz treh) clienta ')]
listok += [input('vvedite HOSTNAME 3-ogo (iz treh) clienta ')]

with open('/etc/rsyslog.conf', 'r') as f:
  old = f.read()

with open('/etc/rsyslog.conf', 'w') as f:
  new1 = old.rapace('#module(load=”imudp”)', 'module(load=”imudp”)')
  new2 = new1.rapace('#input(type=”imudp” port=”514”)', 'input(type=”imudp” port=”514”)')

for i in range(len(listok)):
  with open('etc/rsyslog.conf', 'a') as f:
    f.write(f'''
if ( $hostname == "{listok[i]}" and $syslogseverity == 2 ) then /opt/logs/{listok[i]}/crit.log
if ( $hostname == "{listok[i]}" and $syslogfacility-text == “auth” ) then /opt/logs/{listok[i]}/auth.log
if ( $hostname == "{listok[i]}"  and $syslogseverity-text == “err” ) then /opt/logs/{listok[i]}/error.log
''')

os.system('systemctl restart rsyslog')

############################################## НИЖЕ - ДЛЯ КЛИЕНТА(ОВ)
import os

ip_srv = input('VVEDITE IP SERVER RSYSLOG: ')

with open('/etc/rsyslog.conf', 'a') as f:
  f.write(f'''
*.=crit @{ ip_srv }
*.=err @{ ip_srv }
*.=info @{ ip_srv }
''')

os.system('systemctl restart rsyslog')

