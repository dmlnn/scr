# -*- coding: utf-8 -*-
#################### для сервера
import os
import subprocess

input('''!!! Скрипт предназначен только для выполнения на Centos         !!!
!!! Перед использованием скрипта ОБЯЗАТЕЛЬНО выполни первое подключение  !!!
!!! по ссш к клиентам вручную для корректной работы скрипта, иначе       !!!
!!! подключать клиентов придется самому (ssh root@IP-CLIENTA)            !!!
!!! Остановить скрипт - Ctrl+C, продолжить - Enter                       !!!
Настройка ssh на клиенте:
apt install ssh -y
nano /etc/ssh/sshd_config
Port 22
PermitRootLogin yes
systemctl restart ssh
!!! Скрипт предназначен только для выполнения на Centos                  !!!
!!! Перед использованием скрипта ОБЯЗАТЕЛЬНО выполни первое подключение  !!!
!!! по ссш к клиентам вручную для корректной работы скрипта, иначе       !!!
!!! подключать клиентов придется самому (ssh root@IP-CLIENTA)            !!!
!!! Остановить скрипт - Ctrl+C, продолжить - Enter                       !!!''')
print("Введи айпи адреса всех трех клиентов через пробел: ")
ip_cl = input().split()
ip_srv = input('Введи айпи этой машины: ')

os.system('apt install sshpass -y')
os.system('yum install sshpass -y')
os.system('systemctl stop firewalld')
os.system('systemctl disable firewalld')

listok = []
for i in ip_cl:
  command = ['sshpass', '-proot', 'ssh', f'root@{i}', 'cat', '/etc/hostname']
  out_h = str(subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0])[2:]
  out_h =out_h[:-3]
  listok += [out_h]

with open('/etc/selinux/config', 'r') as f:
  old = f.read()
  
with open('/etc/selinux/config', 'w') as f:
  new = old.replace('SELINUX=enforcing', 'SELINUX=disabled')
  f.write(new)

with open('/etc/rsyslog.conf', 'r') as f:
  old = f.read()

with open('/etc/rsyslog.conf', 'w') as f:
  new1 = old.replace('#module(load="imudp")', 'module(load="imudp")')
  new2 = new1.replace('#input(type="imudp" port="514")', 'input(type="imudp" port="514")')
  new3 = new2.replace('#$ModLoad imudp', '$ModLoad imudp')
  new4 = new3.replace('#$UDPServerRun 514', '$UDPServerRun 514')
  f.write(new4)

for i in range(len(listok)):
  with open('/etc/rsyslog.conf', 'a') as f:
    f.write(f'''
if ( $hostname == "{listok[i]}" and $syslogseverity == 2 ) then /opt/logs/{listok[i]}/crit.log
if ( $hostname == "{listok[i]}" and $syslogfacility-text == "auth" ) then /opt/logs/{listok[i]}/auth.log
if ( $hostname == "{listok[i]}"  and $syslogseverity-text == "err" ) then /opt/logs/{listok[i]}/error.log
''')

os.system('systemctl restart rsyslog')

agentik = (f"""# -*- coding: utf-8 -*-
import os

with open('/etc/rsyslog.conf', 'a') as f:
  f.write(f'''
*.=crit @{ ip_srv }
*.=err @{ ip_srv }
*.=info @{ ip_srv }
''')

os.system('systemctl restart rsyslog')""")

with open('scr-main/agent_syslog', 'w+') as f:
  f.write(agentik)

for i in ip_cl:
  os.system(f'sshpass -proot scp scr-main/agent_syslog root@{i}:/etc')
  os.system(f'sshpass -proot ssh root@{i} yum install python3 -y')
  os.system(f'sshpass -proot ssh root@{i} python3 /etc/agent_syslog')
