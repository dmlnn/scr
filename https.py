# -*- coding: utf-8 -*-
import os
import subprocess

input('''
!!! Pered ispolzovaniem scripta ybedis 4to na cliente nastroen ssh !!!
apt install ssh -y
nano /etc/ssh/sshd_config
Port 22
PermitRootLogin yes
systemctl restart ssh
''')
command = ['hostname','-I']
output_com = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
ip_srv = str(output_com).split()[1]
name = input('Name for your site(www.example.local): ')
ip_cl = input('ip clienta: ')
os_cl = input('y clienta debian ili centos?(1 or 2): ')
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

with open('/etc/httpd/conf/httpd.conf', 'a') as f:
  f.write(''' 
RewriteEngine On 
RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URL} 
''')

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
input("Sei4as bydyt generirovatsya klu4i, gde passphare pishi root, a ostalnoe mojesh ostavit pystim")
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
os.system(f'scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_cl}:/etc/')
if os_cl == "1": debian()
elif os_cl == "2": centos()
else: print("Nevravilno vvedena os clienta, podkluchai ego sam")
def debian():
  os.system(f'sshpass -proot root@{ip_cl} apt install ca-certificates lynx -y')
  os.system(f'sshpass -proot root@{ip_cl} cp /etc/ca.crt /usr/local/share/ca-certificates/')
  os.system(f'sshpass -proot root@{ip_cl} update-ca-certificates')
  os.system(f'sshpass -proot root@{ip_cl} echo {ip_srv} {name} >> /etc/hosts')
def centos():
  os.system(f'sshpass -proot root@{ip_cl} yum install ca-certificates lynx -y')
  os.system(f'sshpass -proot root@{ip_cl} cp /etc/ca.crt /etc/pki/ca-trust/source/anchors')
  os.system(f'sshpass -proot root@{ip_cl} update-ca-trust')
  os.system(f'sshpass -proot root@{ip_cl} echo {ip_srv} {name} >> /etc/hosts')
  
print(f'Proverka na cliente: lynx {name}')
