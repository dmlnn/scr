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

name = input('Адрес твоего сайта(www.example.local): ')
ip_srv = input("ip веб-сервера: ")
ip_cl = input('ip клиента: ')

name_vars = 'root@' + name.split('.')[1] + '.' + name.split('.')[2]

os.system('systemctl disable firewalld') 
os.system('systemctl stop firewalld') 
os.system('yum install httpd mod_ssl sshpass -y') 
os.system('mkdir /var/www/html/out') 
os.system(f'echo {name} > /var/www/html/out/index.html') 

with open('/etc/httpd/conf/httpd.conf', 'r') as f:
  old = f.read()

with open('/etc/httpd/conf/httpd.conf', 'w') as f:
  new1 = old.replace('DocumentRoot "/var/www/html"', 'DocumentRoot "/var/www/html/out"')
  f.write(new1)
  
with open('/etc/httpd/conf/httpd.conf', 'r') as f:
  old = f.read()
 
with open('/etc/httpd/conf/httpd.conf', 'w') as f:
  new2 = old.replace('<Directory "/var/www/html/">', '<Directory "/var/www/html/out">')
  f.write(new2)

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
input("Сейчас будут генерироваться ключи, где pass phrase введи root, где попросят yes пиши yes, поля common name можешь оставить пустыми")
os.system('./easyrsa init-pki')
os.system('./easyrsa build-ca') 
os.system(f'./easyrsa gen-req {name} nopass')
os.system(f'./easyrsa sign-req server {name}')
os.chdir('/root')
os.system(f'cp /etc/openvpn/easy-rsa/3/pki/private/{name}.key /etc/')
os.system(f'cp /etc/openvpn/easy-rsa/3/pki/issued/{name}.crt /etc/')

with open('/etc/httpd/conf.d/ssl.conf', 'r') as f:
  old = f.read()

with open('/etc/httpd/conf.d/ssl.conf', 'w') as f:
  new1 = old.replace('SSLCertificateFile /etc/pki/tls/certs/localhost.crt', f'SSLCertificateFile /etc/{name}.crt')
  f.write(new1)

with open('/etc/httpd/conf.d/ssl.conf', 'r') as f:
  old = f.read()
  
with open('/etc/httpd/conf.d/ssl.conf', 'w') as f:
  new2 = old.replace('SSLCertificateKeyFile /etc/pki/tls/private/localhost.key', f'SSLCertificateKeyFile /etc/{name}.key')
  f.write(new2)
  
with open('/etc/selinux/config', 'r') as f:
  old = f.read()
  
with open('/etc/selinux/config', 'w') as f:
  new = old.replace('SELINUX=enforcing', 'SELINUX=disabled')
  f.write(new)
  
os.system('systemctl restart httpd') 
os.system(f'sshpass -proot scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_cl}:/etc')

def debian():
  hostiki = f'''import os

os.system('apt install ca-certificates lynx -y')
os.system('cp /etc/ca.crt /usr/local/share/ca-certificates/')
os.system('update-ca-certificates')
with open('/etc/hosts', 'a') as f: f.write("{ip_srv} {name}")
os.system('cat /etc/hosts')'''
  with open('scr-main/agent_https', 'w+') as f:
    f.write(hostiki)
  os.system(f'sshpass -proot scp scr-main/agent_https root@{ip_cl}:/etc')
  print('Agent otrabotal')
  
def centos():
  os.system(f'sshpass -proot ssh root@{ip_cl} yum install python3 -y')
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
  

command = ['sshpass', '-proot', 'ssh', f'root@{ip_cl}', 'cat', '/proc/version']
output_com = str(subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0])
if 'Red Hat' in output_com: centos()
else: debian()

os.system(f'sshpass -proot ssh root@{ip_cl} python3 /etc/agent_https')

print(f'\nМожно проверять на клиенте(lynx {name})')
