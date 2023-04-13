# -*- coding: utf-8 -*-
import os
import subprocess
import ipaddress

input('''
!!! Скрипт предназначен только для выполнения на Centos                  !!!
!!! Перед использованием скрипта ОБЯЗАТЕЛЬНО выполни первое подключение  !!!
!!! по ссш к клиентам вручную для корректной работы скрипта, иначе       !!!
!!! подключать клиентов придется самому (ssh root@IP-CLIENTA)            !!!
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
''')
srv_vpn = input('Сервер впн будет на этой машине?(y/n)')
ip_cl = input('Введи ip vpn-клиента: ')
ip_vpn = input('Введи ip для самого vpn например 5.5.5.0: ')
vpn_srv = 

settings_vpn = f'''
import os

'''

def yd_server():                           # Если сервер впн не совпадает с центром сертификации
  
def server_vpn():                          # Если сервер впн совпадает с центром сертификации
  
if srv_vpn == 'y': server_vpn()
else: yd_server()

def cert():                                 # Центр сертификации
  os.system('yum install epel-release -y')
  os.system('yum update -y')
  os.system('yum install easy-rsa openvpn -y')
  os.system('cp -r /usr/share/easy-rsa /etc/openvpn/')
  os.chdir('/etc/openvpn/easy-rsa/3')
  with open('vars', 'w+') as f:
    f.write(f'''set_var EASYRSA                "$PWD"
set_var EASYRSA_PKI               "$EASYRSA/pki"
set_var EASYRSA_DN                "cn_only"
set_var EASYRSA_REQ_COUNTRY       "RU"
set_var EASYRSA_REQ_PROVINCE      "MSK"
set_var EASYRSA_REQ_CITY          "MSK"
set_var EASYRSA_REQ_ORG           "KMPO"
set_var EASYRSA_REQ_EMAIL         "{name_vars}"
set_var EASYRSA_REQ_OU            "IT"
set_var EASYRSA_KEY_SIZE          4096
set_var EASYRSA_ALGO              rsa
set_var EASYRSA_CA_EXPIRE         7500
set_var EASYRSA_CERT_EXPIRE       3650
set_var EASYRSA_NS_SUPPORT        "no"
set_var EASYRSA_NS_COMMENT        "CERTIFICATE AUTHORITY"
set_var EASYRSA_EXT_DIR           "$EASYRSA/x509-types"
set_var EASYRSA_SSL_CONF          "$EASYRSA/openssl-1.0.cnf"
set_var EASYRSA_DIGEST            "sha512"''')
  os.system('chmod +x vars')
  input("Сейчас будут генерироваться ключи, где passphare введи root, где попросят yes пиши yes, поля common name можешь оставить пустыми")
  os.system('./easyrsa init-pki')
  os.system('./easyrsa build-ca') 
  os.system('./easyrsa gen-req serv nopass')
  os.system('./easyrsa sign-req server serv')
  os.system('./easyrsa gen-req client nopass')
  os.system('./easyrsa sign-req server client')
  os.system('./easyrsa gen-dh')
  os.system('openvpn --genkey --secret ta.key')
  os.chdir('/root')


os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_cl}:/etc')


def centos():
  hostiki = f'''import os

os.system('yum install ca-certificates lynx -y')
os.system('cp /etc/ca.crt /etc/pki/ca-trust/source/anchors')
os.system('update-ca-trust')
with open('/etc/hosts', 'a') as f: f.write("{ip_srv} {name}")
os.system('cat /etc/hosts')'''
  with open('scr-main/agent_https', 'w+') as f:
    f.write(hostiki)
  os.system(f'sshpass -proot scp scr-main/agent_https root@{ip_cl}:/etc')
  print('Agent otrabotal')
  
  
if os_cl == "1": debian()
elif os_cl == "2": centos()
else: print("Неправильно введена ос клиента, придется подключать его вручную")

os.system(f'sshpass -proot ssh root@{ip_cl} python3 /etc/agent_https')

print(f'Можно проверять на клиенте(lynx {name})')
