# -*- coding: utf-8 -*-
#################### для сервера
import os



listok = []

listok += [input('Введи HOSTNAME первого (из трех) клиента: ')]
listok += [input('Введи HOSTNAME второго (из трех) клиента: ')]
listok += [input('Введи HOSTNAME первого (из трех) клиента: ')]
ip_srv = input('Введи айпи сервера для логов: ')

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

agentik = (f'''# -*- coding: utf-8 -*-
import os

with open('/etc/rsyslog.conf', 'a') as f:
  f.write(f'''
*.=crit @{ ip_srv }
*.=err @{ ip_srv }
*.=info @{ ip_srv }
''')

os.system('systemctl restart rsyslog')''')

with open('scr-main/agent_syslog', 'w+') as f:
  f.write(agentik)

os.system('apt install sshpass -y')
os.system('yum install sshpass -y')

os.system(f'sshpass -proot scp scr-main/agent_syslog root@{listok[0]}')
os.system(f'sshpass -proot scp scr-main/agent_syslog root@{listok[1]}')
os.system(f'sshpass -proot scp scr-main/agent_syslog root@{listok[2]}')
