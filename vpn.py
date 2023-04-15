# -*- coding: utf-8 -*-
import os
import subprocess

input('''
!!! Скрипт предназначен только для выполнения на Centos                  !!!
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
!!! Остановить скрипт - Ctrl+C, продолжить - Enter                       !!!
''')

ip_srv = input('Введи ip сервера для vpn: ')
ip_cl = input('Введи ip клиента для vpn: ')
print('Введи ip для самого vpn обязательно с 0 на конце, например 5.5.5.0: ')
ip_vpn = input()    
os_vpn_cl = ''
while ((os_vpn_cl != 'centos') & (os_vpn_cl != 'debian')):
    os_vpn_cl = input('Ввебди ОС клиента (centos/debian): ').lower()
    
                                           # Конфиги впна для сервера и клиента 
params_vpn_serv = (f'''port 1122
proto udp
dev tun

dh /etc/openvpn/server/dh.pem
ca /etc/openvpn/server/ca.crt
cert /etc/openvpn/server/serv.crt
key /etc/openvpn/server/serv.key
tls-auth /etc/openvpn/server/ta.key 0	
 
server {ip_vpn} 255.255.255.224
 
ifconfig-pool-persist ipp.txt

keepalive 10 120
user nobody
group nogroup
 
persist-key
persist-tun
 
status /var/log/openvpn-status.log
log /var/log/openvpn.log
log-append /var/log/openvpn.log
verb 3
 
explicit-exit-notify 1
cipher AES-128-CBC
auth SHA256''')

params_vpn_cl = (f'''client
dev tun
proto udp
remote {ip_srv} 1122
resolv-retry infinite
nobind	
user nobody
group nobody
persist-key
persist-tun
ca /etc/openvpn/client/ca.crt    	
cert /etc/openvpn/client/client.crt
key /etc/openvpn/client/client.key 
tls-auth /etc/openvpn/client/ta.key 1
remote-cert-tls server
cipher AES-128-CBC
auth SHA256''')



                                           # Настройка впна на дебиане если он сервер
install_vpn_deb_srv =(f'''import os

os.system('apt install openvpn -y')
with open('/etc/openvpn/server.conf', 'w') as f:
    f.write("""{params_vpn_serv}""")
''')

                                           # Настройка впна на дебиане если он клиент
install_vpn_deb_cl =(f'''import os

os.system('apt install openvpn -y')
with open('/etc/openvpn/client.conf', 'w+') as f:
    f.write("""{params_vpn_cl}""")
''')

                                           # Настройка впна на центосе клиенте
install_vpn_cent_cl =(f'''import os

os.system('yum install epel-release -y')
os.system('yum update -y')
os.system('yum install openvpn -y')
with open('/etc/openvpn/client.conf', 'w+') as f:
    f.write("""{params_vpn_cl}""")
''')

def cert():                                 # Центр сертификации
  os.system('yum install epel-release -y')
  os.system('yum update -y')
  os.system('yum install easy-rsa openvpn -y')
  os.system('cp -r /usr/share/easy-rsa /etc/openvpn/')
  os.chdir('/etc/openvpn/easy-rsa/3')
  with open('vars', 'w+') as f:
    f.write('''set_var EASYRSA                "$PWD"
set_var EASYRSA_PKI               "$EASYRSA/pki"
set_var EASYRSA_DN                "cn_only"
set_var EASYRSA_REQ_COUNTRY       "RU"
set_var EASYRSA_REQ_PROVINCE      "MSK"
set_var EASYRSA_REQ_CITY          "MSK"
set_var EASYRSA_REQ_ORG           "KMPO"
set_var EASYRSA_REQ_EMAIL         "root@kmpo.local"
set_var EASYRSA_REQ_OU            "IT"
set_var EASYRSA_KEY_SIZE          2048
set_var EASYRSA_ALGO              rsa
set_var EASYRSA_CA_EXPIRE         7500
set_var EASYRSA_CERT_EXPIRE       3650
set_var EASYRSA_NS_SUPPORT        "no"
set_var EASYRSA_NS_COMMENT        "CERTIFICATE AUTHORITY"
set_var EASYRSA_EXT_DIR           "$EASYRSA/x509-types"
set_var EASYRSA_SSL_CONF          "$EASYRSA/openssl-1.0.cnf"
set_var EASYRSA_DIGEST            "sha512"''')
  os.system('chmod +x vars')
  input("Сейчас будут генерироваться ключи, где pass phrase введи root, где попросят yes пиши yes, поля common name можешь оставить пустыми")
  os.system('./easyrsa init-pki')
  os.system('./easyrsa build-ca') 
  os.system('./easyrsa gen-req serv nopass')
  os.system('./easyrsa sign-req server serv')
  os.system('./easyrsa gen-req client nopass')
  os.system('./easyrsa sign-req client client')
  os.system('./easyrsa gen-dh')
  os.system('openvpn --genkey --secret ta.key')
  os.chdir('/root')

  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_srv}:/etc/openvpn/server')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/dh.pem root@{ip_srv}:/etc/openvpn/server')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/issued/serv.crt root@{ip_srv}:/etc/openvpn/server')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/private/serv.key root@{ip_srv}:/etc/openvpn/server')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/ta.key root@{ip_srv}:/etc/openvpn/server')
  
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_cl}:/etc/openvpn/client')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/issued/client.crt root@{ip_cl}:/etc/openvpn/client')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/private/client.key root@{ip_cl}:/etc/openvpn/client')
  os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/ta.key root@{ip_cl}:/etc/openvpn/client')
  
def scr_srv():                                      # Создание и отправка агента на сервер впн
  with open('scr-main/agent_vpn_srv', 'w+') as f:
    f.write(install_vpn_deb_srv)
  os.system(f'sshpass -proot scp scr-main/agent_vpn_srv root@{ip_srv}:/etc')
  os.system(f'sshpass -proot ssh root@{ip_srv} apt install python3 -y')
  os.system(f'sshpass -proot ssh root@{ip_srv} python3 /etc/agent_vpn_srv')

def scr_cl_cent():                                       # Создание и отправка агента на клиента центоса впн
  with open('scr-main/agent_vpn_cl', 'w+') as f:
    f.write(install_vpn_cent_cl)
  os.system(f'sshpass -proot scp scr-main/agent_vpn_cl root@{ip_cl}:/etc')
  os.system(f'sshpass -proot ssh root@{ip_cl} yum install python3 -y')
  os.system(f'sshpass -proot ssh root@{ip_cl} python3 /etc/agent_vpn_cl')

def scr_cl_deb():                                      # Создание и отправка агента на клиента дебиана впн
  with open('scr-main/agent_vpn_cl', 'w+') as f:
    f.write(install_vpn_deb_cl)
  os.system(f'sshpass -proot scp scr-main/agent_vpn_srv root@{ip_srv}:/etc')
  os.system(f'sshpass -proot ssh root@{ip_srv} apt install python3 -y')
  os.system(f'sshpass -proot ssh root@{ip_srv} python3 /etc/agent_vpn_srv')
  
os.system('yum install sshpass -y')
scr_srv()
if os_vpn_cl == "centos": scr_cl_cent()
else: scr_cl_deb()
cert()

os.system(f'sshpass -proot ssh root@{ip_srv} systemctl restart openvpn@server')
os.system(f'sshpass -proot ssh root@{ip_cl} systemctl restart openvpn@client')

print('VPN настроен')
