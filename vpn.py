# -*- coding: utf-8 -*-
import os

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
srv_vpn = input('Сервер впн будет на этой машине?(y/n)')
print('Введи айпи адрес сервера для впн если он на этой машине, то адрес этой машины: ')
ip_srv = input()
ip_cl = input('Введи ip vpn-клиента: ')
print('Введи ip для самого vpn обязательно с 0 на конце, например 5.5.5.0: ')
ip_vpn = input()
print('Введи ос сервера и клиента маленькими буквами(debian/centos)')
os_vpn_srv = input('Server: ')
os_vpn_cl = input('Client: ')
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
ca /еtc/openvpn/client/ca.crt    	
cert /etc/openvpn/client/client.crt
key /etc/openvpn/client/client.key 
tls-auth /etc/openvpn/client/ta.key 1
remote-cert-tls server
cipher AES-128-CBC
auth SHA256''')
                                           # Подготовка для впна на дебиане
install_vpn_deb =(f'''import os

os.system('apt install openvpn -y')
os.system('zcat /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz > /etc/openvpn/server.conf')
with open('/etc/openvpn/server.conf') as f:
    f.write('')
''')

                                           # Подготовка для впна на центосе
install_vpn_cent =()

def yd_server():                           # Если сервер впн не совпадает с центром сертификации
  ()
def server_vpn():                          # Если сервер впн совпадает с центром сертификации
  ()
if srv_vpn == 'y': server_vpn()
else: yd_server()

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
