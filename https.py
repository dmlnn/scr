# -*- coding: utf-8 -*-
import os

name = input('Name for your site(www.example.local): ')
ip_cl = input('ip clienta: ')
os.system('systemctl disable firewalld') 
os.system('systemctl stop firewalld') 
os.system('yum install httpd mod_ssl -y') 
os.system('mkdir /var/www/html/out') 
os.system(f'echo {name} > /var/www/html/out/index.html') 

with open('/etc/httpd/conf/httpd.conf', 'w+') as f:
  old = f.read()
  new1 = old.replace('DocumentRoot “/var/www/html/"', 'DocumentRoot “/var/www/html/out”')
  new2 = old.replace('<Directory “/var/www/html/">', '<Directory “/var/www/html/out”>')
  f.write(new1)
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
os.system('cd /etc/openvpn/easy-rsa/3/')
with open('vars', 'w+') as f:
  f.write('''set_var EASYRSA “$PWD”
set_var EASYRSA_PKI “$EASYRSA/pki”
set_var EASYRSA_DN “cn_only”
set_var EASYRSA_REQ_COUNTRY    “RU”
set_var EASYRSA_REQ_PROVINCE    “MSK”
set_var EASYRSA_REQ_CITY    “MSK”
set_var EASYRSA_REQ_ORG “WorldSkills Russia”
set_var EASYRSA_REQ_EMAIL    “root@skill39.wsr”
set_var EASYRSA_REQ_OU    “IT”
set_var EASYRSA_KEY_SIZE 4096
set_var EASYRSA_ALGO        rsa
set_var EASYRSA_CA_EXPIRE    7500
set_var EASYRSA_CERT_EXPIRE    3650
set_var EASYRSA_NS_SUPPORT        “no”
set_var EASYRSA_NS_COMMENT    “CERTIFICATE AUTHORITY”
set_var EASYRSA_EXT_DIR    “$EASYRSA/x509-types”
set_var EASYRSA_SSL_CONF    “$EASYRSA/openssl-1.0.conf”
set_var EASYRSA_DIGES    “sha512”''')
os.system('chmod +x vars')
os.system('/etc/openvpn/easy-rsa/3/./easyrsa /etc/openvpn/easy-rsa/3/init-pki')
os.system('/etc/openvpn/easy-rsa/3/./easyrsa /etc/openvpn/easy-rsa/3/build-ca') 
os.system(f'/etc/openvpn/easy-rsa/3/./easyrsa /etc/openvpn/easy-rsa/3/gen-req {name} nopass')
os.system(f'/etc/openvpn/easy-rsa/3/./easyrsa /etc/openvpn/easy-rsa/3/sign-req server {name}')
os.system(f'cp /etc/openvpn/easy-rsa/3/pki/private/{name}.key /etc/')
os.system(f'cp /etc/openvpn/easy-rsa/3/pki/issued/{name}.crt /etc/')

with open('/etc/httpd/conf.d/ssl.conf', 'w+') as f:
  old = f.read()
  new1 = old.replace(f'SSLCertificateFile /etc/openvpn/easy-rsa/3/pki/issued/{name}.crt', f'SSLCertificateFile /etc/{name}.crt')
  new2 = old.replace(f'SSLCertificateKeyFile /etc/openvpn/easy-rsa/3/pki/private/{name}.key', f'SSLCertificateKeyFile /etc/{name}.key')
  f.write(new1)
  f.write(new2)
 
with open('/etc/selinux/config', 'w+') as f:
  f.write((f.read()).replace('SELINUX=enforcing', 'SELINUX=disabled'))

os.system('systemctl restart httpd') 
os.system(f'scp /etc/openvpn/easy-rsa/3/pki/ca.crt root@{ip_cl}:/etc/openvpn/client/')
print(f'Your site: {name}')
