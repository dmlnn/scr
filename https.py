# -*- coding: utf-8 -*-
import os

os.system('systemctl disable firewalld') 
os.system('systemctl stop firewalld') 
os.system('yum install httpd mod_ssl -y') 
os.system('mkdir /var/www/html/out') 
os.system('echo example.local > /var/www/html/out/index.html') 

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
os.system('cd /etc/openvpn/easy-rsa/3/')
os.system('./easyrsa init-pki')
os.system('./easyrsa build-ca') 
os.system('./easyrsa gen-req www.example.local nopass')
os.system('./easyrsa sign-req server www.example.local')
os.system('cp /etc/openvpn/easy-rsa/3/pki/private/www.example.ru.key /etc/')
os.system('cp /etc/openvpn/easy-rsa/3/pki/issued/www.example.ru.crt /etc/')

with open('/etc/httpd/conf.d/ssl.conf', 'w+') as f:
  old = f.read()
  new1 = old.replace('SSLCertificateFile /etc/openvpn/easy-rsa/3/pki/issued/www.example.local.crt', 'SSLCertificateFile /etc/www.examle.local.crt')
  new2 = old.replace('SSLCertificateKeyFile /etc/openvpn/easy-rsa/3/pki/private/www.example.local.key', 'SSLCertificateKeyFile /etc/www.examle.local.key')
  f.write(new1)
  f.write(new2)
 
with open('/etc/selinux/config', 'w+') as f:
  f.write((f.read()).replace('SELINUX=enforcing', 'SELINUX=disabled'))

os.system('systemctl restart httpd') 
os.system('cp /etc/openvpn/easy-rsa/3/pki/ca.crt root@IP-client:/etc/openvpn/client/')
